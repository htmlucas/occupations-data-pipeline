output "bucket_name" {
  description = "Name of the S3 bucket used by the occupations pipeline."
  value       = aws_s3_bucket.occupations.bucket
}

output "bucket_arn" {
  description = "ARN of the S3 bucket used by the occupations pipeline."
  value       = aws_s3_bucket.occupations.arn
}