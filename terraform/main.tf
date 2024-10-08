provider "aws" {
    region     = var.REGION
    secret_key = var.AWS_SECRET_ACCESS_KEY
    access_key = var.AWS_ACCESS_KEY
}

# =========================== DATA ===========================
data "aws_vpc" "c13-vpc" { id = var.VPC_ID }
data "aws_subnet" "c13-public-subnet1" { id = var.SUBNET_ID1 }
data "aws_subnet" "c13-public-subnet2" { id = var.SUBNET_ID2 }
data "aws_subnet" "c13-public-subnet3" { id = var.SUBNET_ID3 }

data "aws_ecr_image" "fox_news_scraper_image" {
    repository_name = "c13-boudicca-mp-fox-news-scraper"
    image_tag       = "latest"
}

data "aws_ecr_image" "democracy_now_news_scraper_image" {
    repository_name = "c13-boudicca-mp-democracy-now-news-scraper"
    image_tag       = "latest"
}

data "aws_ecr_image" "article_combiner_image" {
    repository_name = "c13-boudicca-mp-article-combiner"
    image_tag       = "latest"
}

data "aws_ecr_image" "email_generator_image" {
    repository_name = "c13-boudicca-mp-email-generator"
    image_tag       = "latest"
}

data "aws_iam_role" "execution_role" { name = "ecsTaskExecutionRole" }
data "aws_ecs_cluster" "c13_cluster" { cluster_name = "c13-ecs-cluster" }

# =========================== Scraping Pipeline ===========================

resource "aws_iam_role" "lambda_execution_role" {
    name               = "c13-boudicca-mp-pipeline-role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Action    = "sts:AssumeRole",
                Effect    = "Allow",
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "lambda_execution_policy_attachment" {
    role       = aws_iam_role.lambda_execution_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "fox_news_scraper_lambda" {
    function_name = "c13-boudicca-mp-fox-news-scraper"
    image_uri     = data.aws_ecr_image.fox_news_scraper_image.image_uri
    role          = aws_iam_role.lambda_execution_role.arn
    package_type = "Image"
    timeout = 900
    memory_size = 256

    image_config { command = ["main.lambda_handler"] }
}


resource "aws_lambda_function" "democracy_news_now_scraper_lambda" {
    function_name = "c13-boudicca-mp-democracy-now-news-scraper"
    image_uri     = data.aws_ecr_image.democracy_now_news_scraper_image.image_uri
    role          = aws_iam_role.lambda_execution_role.arn

    package_type = "Image"

    timeout = 900
    memory_size = 256

    image_config { command = ["main.lambda_handler"] }
}

resource "aws_lambda_function" "article_combiner_lambda" {
    function_name = "c13-boudicca-mp-article-combiner"
    image_uri     = data.aws_ecr_image.article_combiner_image.image_uri
    role          = aws_iam_role.lambda_execution_role.arn
    package_type = "Image"
    timeout = 900
    memory_size = 256

    image_config { command = ["main.lambda_handler"] }
}

resource "aws_lambda_function" "email_generator_lambda" {
    function_name = "c13-boudicca-mp-email-generator"
    image_uri     = data.aws_ecr_image.email_generator_image.image_uri
    role          = aws_iam_role.lambda_execution_role.arn
    package_type = "Image"
    timeout = 900
    memory_size = 256

    image_config { command = ["main.lambda_handler"] }
}