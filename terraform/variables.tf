variable "REGION" {
    type = string 
    default = "eu-west-2"
}

variable "VPC_ID" {type = string}
variable "SUBNET_ID1" {type = string}
variable "SUBNET_ID2" {type = string}
variable "SUBNET_ID3" {type = string}

variable "AWS_ACCESS_KEY" {type = string}
variable "AWS_SECRET_ACCESS_KEY" {type = string}

variable "FOX_NEWS_SCRAPER_ECR_REPO" {type = string}
variable "DEMOCARCY_NOW_SCRAPER_ECR_REPO" {type = string}
variable "ARTICLE_COMBINER_ECR_REPO" {type = string}
variable "EMAIL_GENERATOR_ECR_REPO" {type = string}
variable "ARTICLE_ANALYSER_ECR_REPO" {type = string}

variable "S3_BUCKET_NAME" {type = string}

variable "DB_HOST" {type = string}
variable "DB_PORT" {type = string}
variable "DB_PASSWORD" {type = string}
variable "DB_USER" {type = string}
variable "DB_NAME" {type = string}