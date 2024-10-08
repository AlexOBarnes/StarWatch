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



# RDS Instance storing data for the StarWatch application. 
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