provider "aws"{
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY 
    secret_key = var.AWS_SECRET_KEY
}

data "aws_vpc" "c13-vpc" {
  id = var.VPC_ID
}

data "aws_subnet" "c13-public-subnet-a" {
  id = var.SUBNET_ID_A
}

data "aws_subnet" "c13-public-subnet-b" {
  id = var.SUBNET_ID_B 
}


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



# RDS - PostgreSQL Instance storing data for the StarWatch application. 
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

# Defining ecah lambda function for the StarWatch project, would lead to 
# a very long and verbose main.tf file. So instead, a lambda function variable
# dictionary has been defined that outlines that name of each pipeline and the 
# ECR image it is using. This way, we can traverse it build lambda functions for each,
# without having to manually list each configuration out.
variable "lambda_functions" {
  type = map(object({
    function_name = string
    image_uri     = string
  }))
  default = {
    weekly_bodies = {
      function_name = "WeeklyAstronomyBodiesPipeline"
      image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c13-tamar-weekly-astronomy-pipeline:latest"
    },
    weekly_sunrise_sunset = {
      function_name = "WeeklySunriseSunsetPipeline"
      image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c13-tamar-weekly-openmeteo:latest"
    },
    hourly_aurora = {
      function_name = "HourlyAuroraWatchPipeline"
      image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c13-tamar-aurorawatch-pipeline:latest"
    },
    hourly_nearest_bodies = {
      function_name = "HourlyNearestBodiesEventsPipeline"
      image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c13-tamar-sms-checker:latest"
    },
    quadhourly_weather = {
      function_name = "QuadhourlyOpenMeteoWeatherPipeline"
      image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c13-tamar-quadhoral-openmeteo:latest"
    }
  }
}

# Lambda Functions beign build, using the lanbda functions variable.
resource "aws_lambda_function" "lambda_functions" {
  for_each = var.lambda_functions

  function_name = each.value.function_name
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  image_uri     = each.value.image_uri
  timeout       = 900
  memory_size   = 512

  environment {
    variables = {
      RDS_HOSTNAME = var.DB_HOST
      DB_NAME      = var.DB_NAME
      DB_USER      = var.DB_USER
      DB_PASSWORD  = var.DB_PASSWORD
    }
  }
}

