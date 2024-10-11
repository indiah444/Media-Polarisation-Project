# Describe information terraform should share with you.

output "EC2_public_dns" {
    value = aws_instance.pipeline_ec2.public_dns
}