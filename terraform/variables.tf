variable "aws_region" {
  description = "AWS region used by the infrastructure."
  type        = string
  default     = "sa-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket used by the occupations pipeline."
  type        = string
}