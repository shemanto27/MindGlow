variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.medium"
}

variable "ami" {
  description = "Ubuntu AMI ID"
  default     = "ami-0a2e7efb4257c0907" # Ubuntu 22.04 LTS (Jammy) in ca-central-1
}

variable "bucket_name" {
  description = "S3 bucket name"
  default     = "mindglow-media-prod"
}

variable "ec2_name" {
  description = "Name tag for EC2 instance"
  default     = "mindglow_server"
}

variable "db_username" {
  description = "RDS Postgres username"
  default     = "mindglow_db"
}

variable "db_password" {
  description = "RDS Postgres password"
  sensitive   = true
  default     = "mindglow_db_password"
}

variable "aws_profile" {
  description = "AWS CLI profile name configured locally"
  default     = "fatima"
}

variable "region" {
  description = "AWS region"
  default     = "ca-central-1"
}