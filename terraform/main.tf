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

# data "aws_ecr_image" "email_generator_image" {
#     repository_name = "c13-boudicca-mp-email-generator"
#     image_tag       = "latest"
# }

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


resource "aws_lambda_function" "democracy_now_news_scraper_lambda" {
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

# resource "aws_lambda_function" "email_generator_lambda" {
#     function_name = "c13-boudicca-mp-email-generator"
#     image_uri     = data.aws_ecr_image.email_generator_image.image_uri
#     role          = aws_iam_role.lambda_execution_role.arn
#     package_type = "Image"
#     timeout = 900
#     memory_size = 256

#     image_config { command = ["main.lambda_handler"] }
# }

resource "aws_iam_role" "step_functions_role" {
  name = "c13-boudicca-mp-main-pipeline-step-functions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "states.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "step_functions_policy" {
  name = "c13-boudicca-mp-main-pipeline-functions-policy"
  role = aws_iam_role.step_functions_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = ["lambda:InvokeFunction"],
        Resource = [
          aws_lambda_function.fox_news_scraper_lambda.arn,
          aws_lambda_function.democracy_now_news_scraper_lambda.arn,
          aws_lambda_function.article_combiner_lambda.arn
        ]
      },
    ]
  })
}

resource "aws_sfn_state_machine" "main_pipeline_state_machine" {
  name     = "c13-boudicca-mp-main-pipeline-state-machine"
  role_arn = aws_iam_role.step_functions_role.arn

  definition = jsonencode({
    StartAt = "SummaryReportTask",
    States = {
      FoxScraperTask = {
        Type = "Task",
        Resource = aws_lambda_function.fox_news_scraper_lambda.arn,
        ResultPath: "$.reportResult",
        Next = "SendEmailTask"
      },
      DemocracyNowScraperTask = {
        Type = "Task",
        Resource = aws_lambda_function.democracy_now_news_scraper_lambda.arn,
        ResultPath: "$.reportResult",
        Next = "SendEmailTask"
      },
      ArticleCombineTask = {
        Type = "Task",
        Resource = aws_lambda_function.article_combiner_lambda.arn,
        ResultPath: "$.reportResult",
        Next = "SendEmailTask"
      }
    }
  })
}

data "aws_iam_policy_document" "step_functions_schedule_trust_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "step_functions_scheduler_role" {
  name               = "c13-boudicca-mp-main-pipeline-step-functions-scheduler-role"
  assume_role_policy = data.aws_iam_policy_document.step_functions_schedule_trust_policy.json
}

resource "aws_iam_role_policy" "step_functions_scheduler_policy" {
  name = "c13-boudicca-mp-main-pipeline-step-functions-scheduler-policy"
  role = aws_iam_role.step_functions_scheduler_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "states:StartExecution",
        Resource = aws_sfn_state_machine.main_pipeline_state_machine.arn
      }
    ]
  })
}

resource "aws_scheduler_schedule" "daily_step_function_trigger" {
  name                       = "c13-boudicca-mp-main-pipeline-schedule"
  schedule_expression        = "cron(0 */1 * * ? *)"
  schedule_expression_timezone = "UTC+01:00"
  flexible_time_window {
    mode = "OFF"
  }
  target {
    arn     = aws_sfn_state_machine.main_pipeline_state_machine.arn
    role_arn = aws_iam_role.step_functions_scheduler_role.arn
    input   = jsonencode({})
  }
}