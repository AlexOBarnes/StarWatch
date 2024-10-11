variable "AWS_REGION" {
  type = string
  default = "eu-west-2"
  
}

variable "AWS_ACCESS_KEY" {
  type = string
  
}

variable "AWS_SECRET_KEY" {
  type = string
  
}

variable "DB_HOST" {
  type = string
  
}


variable "DB_NAME" {
  type = string
  
}

variable "DB_USER" {
  type = string
  
}


variable "DB_PASSWORD" {
  type = string
  sensitive   = true
  
}

variable "VPC_ID" {
    type = string
    sensitive   = true
}


variable "SUBNET_ID_A" {
    type = string
}


variable "SUBNET_ID_B" {
    type = string
}


variable "WEEKLY_ASTRONOMY_IMAGE_URI" {
    type = string
}

variable "WEEKLY_SET_RISE_IMAGE_URI" {
    type = string
}

variable "HOURLY_AURORA_IMAGE_URI" {
    type = string
}

variable "HOURLY_VISIBLE_IMAGE_URI" {
    type = string
}

variable "QUADHOURLY_WEATHER_IMAGE_URI" {
    type = string
}


variable "DASHBOARD_IMAGE_URI" {
    type = string
}

variable "CLUSTER_NAME" {
    type = string
}


variable "NASA_API_KEY" {
  type = string
  sensitive   = true
  
}



variable "ASTRONOMY_ID" {
  type = string
  sensitive   = true
  
}

variable "ASTRONOMY_SECRET" {
  type = string
  sensitive   = true
  
}
