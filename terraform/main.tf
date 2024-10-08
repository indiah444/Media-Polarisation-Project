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
    repository_name = var.FOX_NEWS_SCRAPER_ECR_REPO
    image_tag       = "latest"
}

data "aws_ecr_image" "democracy_now_news_scraper_image" {
    repository_name = var.DEMOCARCY_NOW_SCRAPER_ECR_REPO
    image_tag       = "latest"
}

# data "aws_ecr_image" "email_generator_image" {
#     repository_name = var.EMAIL_GENERATOR_ECR_REPO
#     image_tag       = "latest"
# }

data "aws_ecr_image" "article_analyser_image" {
    repository_name = var.ARTICLE_ANALYSER_ECR_REPO
    image_tag       = "latest"
}

data "aws_s3_bucket" "article_s3_bucket" {bucket = var.S3_BUCKET_NAME}  # may not be needed
data "aws_iam_role" "execution_role" { name = "ecsTaskExecutionRole" }
data "aws_ecs_cluster" "c13_cluster" { cluster_name = "c13-ecs-cluster" }

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

    environment {
        variables = {
            S3_BUCKET_NAME = var.S3_BUCKET_NAME
            AWS_ACCESS_KEY_BOUDICCA = var.AWS_ACCESS_KEY
            AWS_ACCESS_SECRET_KEY_BOUDICCA = var.AWS_SECRET_ACCESS_KEY
        }
    }

    image_config { command = ["main.lambda_handler"] }
}


resource "aws_lambda_function" "democracy_now_news_scraper_lambda" {
    function_name = "c13-boudicca-mp-democracy-now-news-scraper"
    image_uri     = data.aws_ecr_image.democracy_now_news_scraper_image.image_uri
    role          = aws_iam_role.lambda_execution_role.arn

    package_type = "Image"

    timeout = 900
    memory_size = 256

    environment {
        variables = {
            S3_BUCKET_NAME = var.S3_BUCKET_NAME
            AWS_ACCESS_KEY_BOUDICCA = var.AWS_ACCESS_KEY
            AWS_ACCESS_SECRET_KEY_BOUDICCA = var.AWS_SECRET_ACCESS_KEY
        }
    }

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

resource "aws_cloudwatch_log_group" "mp_article_analyser_log_group" {
    name = "/ecs/c13-boudicca-mp-article-analyser"
}

resource "aws_ecs_task_definition" "mp_article_analyser" {
    family                   = "c13-boudicca-mp-article-analyser-task-definition"
    requires_compatibilities = ["FARGATE"]
    network_mode             = "awsvpc"
    cpu                      = "256"
    memory                   = "1024"
    execution_role_arn       = data.aws_iam_role.execution_role.arn

    container_definitions = jsonencode([
        {
            name      = "mp-article-analyser"
            image     = data.aws_ecr_image.article_analyser_image.image_uri
            essential = true
            memory    = 1024
            environment = [
                {
                    name  = "AWS_ACCESS_KEY"
                    value = var.AWS_ACCESS_KEY
                },
                {
                    name  = "AWS_SECRET_KEY"
                    value = var.AWS_SECRET_ACCESS_KEY
                },
                {
                    name  = "BUCKET_NAME"
                    value = var.S3_BUCKET_NAME
                },
                {
                    name  = "REGION"
                    value = var.REGION
                },
                {
                    name  = "DB_HOST"
                    value = var.DB_HOST
                },
                {
                    name  = "DB_PORT"
                    value = var.DB_PORT
                },
                {
                    name  = "DB_USER"
                    value = var.DB_USER
                },
                {
                    name  = "DB_PASSWORD"
                    value = var.DB_PASSWORD
                },
                {
                    name  = "DB_NAME"
                    value = var.DB_NAME
                },
            ]
            logConfiguration = {
                logDriver = "awslogs"
                options = {
                    awslogs-group         = "/ecs/c13-boudicca-mp-article-analyser"
                    awslogs-region        = var.REGION
                    awslogs-stream-prefix = "ecs"
                }
            }
        }
    ])
}

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
          aws_lambda_function.democracy_now_news_scraper_lambda.arn
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "ecs:RunTask",
          "ecs:StopTask",
          "ecs:DescribeTasks",
          "iam:PassRole"
        ],
        Resource = [
          data.aws_iam_role.execution_role.arn,
          aws_ecs_task_definition.mp_article_analyser.arn
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "ecs:DescribeClusters",
          "ecs:DescribeTaskDefinition",
          "ecs:DescribeTasks",
          "ecs:ListTasks"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "events:PutRule",
          "events:DeleteRule",
          "events:DescribeRule",
          "events:EnableRule",
          "events:DisableRule",
          "events:PutTargets",
          "events:RemoveTargets"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:CreateLogGroup"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_sfn_state_machine" "main_pipeline_state_machine" {
  name     = "c13-boudicca-mp-main-pipeline-state-machine"
  role_arn = aws_iam_role.step_functions_role.arn

  definition = jsonencode({
    StartAt = "ParallelScraping",
    States = {
      ParallelScraping = {
        Type = "Parallel",
        Branches = [
          {
            StartAt = "FoxScraperTask",
            States = {
              FoxScraperTask = {
                Type = "Task",
                Resource = aws_lambda_function.fox_news_scraper_lambda.arn,
                ResultPath = "$.foxNewsResult",
                End = true
              }
            }
          },
          {
            StartAt = "DemocracyNowScraperTask",
            States = {
              DemocracyNowScraperTask = {
                Type = "Task",
                Resource = aws_lambda_function.democracy_now_news_scraper_lambda.arn,
                ResultPath = "$.democracyNowResult",
                End = true
              }
            }
          }
        ],
        ResultPath = "$.scrapingResults",
        Next = "RunArticleAnalyserECS"
      },
      RunArticleAnalyserECS = {
        Type = "Task",
        Resource = "arn:aws:states:::ecs:runTask.sync",
        Parameters = {
          Cluster = "${data.aws_ecs_cluster.c13_cluster.cluster_name}",
          TaskDefinition = "${aws_ecs_task_definition.mp_article_analyser.arn}",
          LaunchType = "FARGATE",
          NetworkConfiguration = {
            AwsvpcConfiguration = {
              Subnets = [
                "${data.aws_subnet.c13-public-subnet1.id}",
                "${data.aws_subnet.c13-public-subnet2.id}",
                "${data.aws_subnet.c13-public-subnet3.id}"
              ],
              AssignPublicIp = "ENABLED"
            }
          }
        },
        ResultPath = "$.ecsRunResult",
        End = true
      }
    }
  })
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