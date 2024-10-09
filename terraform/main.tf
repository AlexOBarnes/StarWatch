# Defining provider.
# AWS access and secret key are passed in a environment
# variables from the terraform.tfvars file.
provider "aws"{
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY 
    secret_key = var.AWS_SECRET_KEY
}


# Cohort 13 designated VPC.
data "aws_vpc" "c13-vpc" {
  id = var.VPC_ID
}


# Two public subnets for the RDS, to 
# ensure the database is robust and highly 
# available across different availablity zones.
data "aws_subnet" "c13-public-subnet-a" {
  id = var.SUBNET_ID_A
}


data "aws_subnet" "c13-public-subnet-b" {
  id = var.SUBNET_ID_B 
}


# Security group for the RDS, dictating valid inbound and outbound traffic.
# Specifically, inbound PostgresSQL traffic on port 5432 and all outbound 
# traffic for database connections.
resource "aws_security_group" "c13-andrew-starwatch-rds-sg" {
    name        = "c13-andrew-starwatch-db-sg"
    vpc_id      = data.aws_vpc.c13-vpc.id

    ingress {
    from_port = 5432
    to_port   = 5432
    protocol = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


# Making a resource for subnet groups, so all used subnets are
# grouped together and so in the future, more subnets can be 
# added to the system in a single place.
resource "aws_db_subnet_group" "c13_rds_subnet_group" {
  name       = "c13-rds-subnet-group"
  subnet_ids = [
    data.aws_subnet.c13-public-subnet-a.id, 
    data.aws_subnet.c13-public-subnet-b.id
  ]

  tags = {
    Name = "c13-rds-subnet-group"
  }
}


# RDS - PostgreSQL Instance storing all data for the StarWatch application. 
resource "aws_db_instance" "default" {
    allocated_storage            = 10
    db_name                      = "tamarstarwatchrds"
    identifier                   = "c13-tamar-starwatch-rds"
    engine                       = "postgres"
    engine_version               = "16.1"
    instance_class               = "db.t3.micro"
    publicly_accessible          = true
    performance_insights_enabled = false
    skip_final_snapshot          = true
    db_subnet_group_name         = aws_db_subnet_group.c13_rds_subnet_group.name
    vpc_security_group_ids       = [aws_security_group.c13-andrew-starwatch-rds-sg.id]
    username                     = var.DB_USER
    password                     = var.DB_PASSWORD
}

# Defining each individual lambda function for the StarWatch project would lead to 
# a very long and verbose main.tf file. Instead, a lambda function dictionary has
# been defined for each Lambda, outlining that name of each pipeline and the 
# ECR image it references. This way, we can traverse it alone to build lambda functions
# for each, without having to manually list each configuration out.
locals {
  lambda_functions = {
    weekly_bodies = {
      function_name = "WeeklyAstronomyBodiesPipeline"
      image_uri     = var.WEEKLY_ASTRONOMY_IMAGE_URI
      invoked_by    = "step_function_weekly"
    },
    weekly_sunrise_sunset = {
      function_name = "WeeklySunriseSunsetPipeline"
      image_uri     = var.WEEKLY_SET_RISE_IMAGE_URI
      invoked_by    = "step_function_weekly"
    },
    hourly_aurora = {
      function_name = "HourlyAuroraWatchPipeline"
      image_uri     = var.HOURLY_AURORA_IMAGE_URI
      invoked_by    = "step_function_hourly"
    },
    hourly_nearest_bodies = {
      function_name = "HourlyNearestBodiesEventsPipeline"
      image_uri     = var.HOURLY_VISIBLE_IMAGE_URI
      invoked_by    = "step_function_hourly"
    },
    quadhourly_weather = {
      function_name = "QuadhourlyOpenMeteoWeatherPipeline"
      image_uri     = var.QUADHOURLY_WEATHER_IMAGE_URI
      invoked_by    = "eventbridge_quadhourly"
    }
  }
}


# The base definition of Lambda function config is defined here, 
# which will be used iteratively to build Lambda pipeline instances.   
resource "aws_lambda_function" "lambda_functions" {
  for_each = local.lambda_functions

  function_name = each.value.function_name
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  image_uri     = each.value.image_uri
  timeout       = 900
  memory_size   = 512

  environment {
    variables = {
      RDS_HOSTNAME = aws_db_instance.default.address # This allows for the RDS address to update dynamically, 
                                                     # in the event we terraform destroy and the address changes.
      DB_NAME      = var.DB_NAME
      DB_USER      = var.DB_USER
      DB_PASSWORD  = var.DB_PASSWORD
    }
  }
}


# EventBridge rule for weekly pipelines (bodies and sunrise/sunset in parallel).
# Triggering step functions, running piplines in parallel.
resource "aws_cloudwatch_event_rule" "weekly_step_function_trigger" {
  name                = "starwatch-weekly-parallel-trigger"
  schedule_expression = "rate(7 days)"
}


# EventBridge rule for hourly pipelines (aurora and nearest bodies in parallel).
# Triggering step functions, running piplines in parallel.
resource "aws_cloudwatch_event_rule" "hourly_step_function_trigger" {
  name                = "starwatch-hourly-parallel-trigger"
  schedule_expression = "rate(1 hour)"
}


# EventBridge rule for quadhourly weather Lambda (direct trigger).
# Triggering the Lambda function directly..
resource "aws_cloudwatch_event_rule" "quadhourly_lambda_trigger" {
  name                = "starwatch-quadhourly-weather-trigger"
  schedule_expression = "rate(4 hours)"
}


# Step Function for Weekly Pipelines (Bodies and Sunrise/Sunset in Parallel).
resource "aws_sfn_state_machine" "weekly_pipelines_step_function" {
    name     = "WeeklyPipelinesParallelExecution"
    role_arn = aws_iam_role.sfn_exec_role.arn

    definition = <<-STATE_MACHINE_DEFINITION
        {
        "StartAt": "ParallelTasks",
        "States": {
            "ParallelTasks": {
            "Type": "Parallel",
            "Branches": [
                {
                "StartAt": "InvokeBodiesLambda",
                "States": {
                    "InvokeBodiesLambda": {
                    "Type": "Task",
                    "Resource": "arn:aws:states:::lambda:invoke",
                    "Parameters": {
                        "FunctionName": "${aws_lambda_function.lambda_functions["weekly_bodies"].arn}"
                    },
                    "End": true
                    }
                }
                },
                {
                "StartAt": "InvokeSunriseSunsetLambda",
                "States": {
                    "InvokeSunriseSunsetLambda": {
                    "Type": "Task",
                    "Resource": "arn:aws:states:::lambda:invoke",
                    "Parameters": {
                        "FunctionName": "${aws_lambda_function.lambda_functions["weekly_sunrise_sunset"].arn}"
                    },
                    "End": true
                    }
                }
                }
            ],
            "End": true
            }
        }
        }
    STATE_MACHINE_DEFINITION
    }


# Step Function for Hourly Pipelines (Aurora and Nearest Bodies/Events in Parallel).
resource "aws_sfn_state_machine" "hourly_pipelines_step_function" {
    name     = "HourlyPipelinesParallelExecution"
    role_arn = aws_iam_role.sfn_exec_role.arn

    definition = <<-STATE_MACHINE_DEFINITION
        {
        "StartAt": "ParallelTasks",
        "States": {
            "ParallelTasks": {
            "Type": "Parallel",
            "Branches": [
                {
                "StartAt": "InvokeAuroraLambda",
                "States": {
                    "InvokeAuroraLambda": {
                    "Type": "Task",
                    "Resource": "arn:aws:states:::lambda:invoke",
                    "Parameters": {
                        "FunctionName": "${aws_lambda_function.lambda_functions["hourly_aurora"].arn}"
                    },
                    "End": true
                    }
                }
                },
                {
                "StartAt": "InvokeNearestBodiesLambda",
                "States": {
                    "InvokeNearestBodiesLambda": {
                    "Type": "Task",
                    "Resource": "arn:aws:states:::lambda:invoke",
                    "Parameters": {
                        "FunctionName": "${aws_lambda_function.lambda_functions["hourly_nearest_bodies"].arn}"
                    },
                    "End": true
                    }
                }
                }
            ],
            "End": true
            }
        }
        }
    STATE_MACHINE_DEFINITION
    }


# EventBridge target to trigger Step Function for weekly pipelines
# Event bridges needs to be maps to a service to trigger.
resource "aws_cloudwatch_event_target" "weekly_parallel_target" {
  rule = aws_cloudwatch_event_rule.weekly_step_function_trigger.name
  arn  = aws_sfn_state_machine.weekly_pipelines_step_function.arn
}


# EventBridge target to trigger Step Function for hourly pipelines
resource "aws_cloudwatch_event_target" "hourly_parallel_target" {
  rule = aws_cloudwatch_event_rule.hourly_step_function_trigger.name
  arn  = aws_sfn_state_machine.hourly_pipelines_step_function.arn
}


# EventBridge target for quadhourly weather Lambda (direct trigger)
resource "aws_cloudwatch_event_target" "quadhourly_weather_target" {
  rule = aws_cloudwatch_event_rule.quadhourly_lambda_trigger.name
  arn  = aws_lambda_function.lambda_functions["quadhourly_weather"].arn
}


# IAM Role for Lambda Execution, to apply policies to 
# (logging, ECR access).
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [{
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }]
  })
}


# IAM Role for Step Functions Execution, to apply policies to.
# (Lambda invoking, logging state transitions).
resource "aws_iam_role" "sfn_exec_role" {
  name = "sfn_exec_role"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [{
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }]
  })
}


# Attaching a basic executon role to Lambdas, to allow for logging.
resource "aws_iam_role_policy_attachment" "lambda_execution_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


# Attaching a basic executon role to step-functions, to allow for logging.
resource "aws_iam_role_policy_attachment" "sfn_logging_policy" {
  role       = aws_iam_role.sfn_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSStepFunctionsLogging"
}


# Lambda functions need read-only access to ECR to pull the container images.
resource "aws_iam_role_policy_attachment" "lambda_ecr_access" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}


# Create the Lambda invoke policy for all indivudal pipeline step functions, iteratively.
# This essentially allowing all step functions in the main.tf to be able to run lambdas.
resource "aws_iam_policy" "sfn_lambda_permission_policy" {
  name   = "sfn_lambda_invoke_policy"
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "lambda:InvokeFunction"
        ],
        "Effect": "Allow",
        "Resource": [for lambda in aws_lambda_function.lambda_functions : lambda.arn]  # Automatically gather all Lambda ARNs
      }
    ]
  })
}


# Attach the above custom policy to the step-functions execution role.
resource "aws_iam_role_policy_attachment" "sfn_lambda_invoke" {
  role       = aws_iam_role.sfn_exec_role.name
  policy_arn = aws_iam_policy.sfn_lambda_permission_policy.arn
}


# This iteratively checks the kind of lambda being assessed, if it's a 
# lambda that is invoked by a step-function, it is provided permissions allowing
# that mapped step-function to run it. However, if the lambda being considered is 
# the quadhourly weather pipeline Lambda, eventbridge is  allowed to trigger it directly,
# as no step function is involved in the running of that pipeline.
resource "aws_lambda_permission" "allow_invoke" {
  for_each = { for key, value in local.lambda_functions : key => value if value.invoked_by != "" }

  statement_id  = "AllowExecutionFrom_${each.value.invoked_by}_${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_functions[each.key].function_name

  principal = each.value.invoked_by == "eventbridge_quadhourly" ? "events.amazonaws.com" : "states.amazonaws.com"

  source_arn = lookup(
    {
      "step_function_weekly"     = aws_sfn_state_machine.weekly_pipelines_step_function.arn
      "step_function_hourly"     = aws_sfn_state_machine.hourly_pipelines_step_function.arn
      "eventbridge_quadhourly"   = aws_cloudwatch_event_rule.quadhourly_lambda_trigger.arn
    },
    each.value.invoked_by,
    ""
  )
}
