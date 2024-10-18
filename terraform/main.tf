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
    repository_name = var.DEMOCRACY_NOW_SCRAPER_ECR_REPO
    image_tag       = "latest"
}

data "aws_ecr_image" "daily_email_image" {
    repository_name = var.DAILY_EMAIL_ECR_REPO
    image_tag       = "latest"
}

data "aws_ecr_image" "weekly_email_image" {
    repository_name = var.WEEKLY_EMAIL_ECR_REPO
    image_tag       = "latest"
}

data "aws_ecr_image" "article_analyser_image" {
    repository_name = var.ARTICLE_ANALYSER_ECR_REPO
    image_tag       = "latest"
}

data "aws_s3_bucket" "article_s3_bucket" {bucket = var.S3_BUCKET_NAME}
data "aws_iam_role" "execution_role" {name = "ecsTaskExecutionRole"}
data "aws_ecs_cluster" "c13_cluster" {cluster_name = var.ECS_CLUSTER_NAME}

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

    image_config { command = ["pipeline_fn.lambda_handler"] }
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

    image_config { command = ["pipeline_dn.lambda_handler"] }
}

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
                {
                    name  = "OPENAI_API_KEY"
                    value = var.OPENAI_API_KEY
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

# =========================== S3 Event to EventBridge ===========================

resource "aws_s3_bucket_notification" "csv_upload_to_s3_notification" {
    bucket     = data.aws_s3_bucket.article_s3_bucket.id
    eventbridge = true
}

resource "aws_cloudwatch_event_rule" "csv_upload_to_s3_event_rule" {
  name        = "c13-boudicca-csv-upload-to-s3-event-rule"
  description = "Triggers ECS Task when new XML file is uploaded to S3"
  event_pattern = jsonencode({
    detail = {
      bucket = {name = ["${data.aws_s3_bucket.article_s3_bucket.id}"]},
      object = {key = [{wildcard = "*_article_data.csv"}]}
    },
    "detail-type" = ["Object Created"],
    source = ["aws.s3"]
  })
}

data "aws_iam_policy_document" "schedule_trust_policy" {
    statement {
        effect = "Allow"
        principals {
            type        = "Service"
            identifiers = ["events.amazonaws.com"]
        }
        actions = ["sts:AssumeRole"]
    }
}

resource "aws_iam_role" "schedule_role" {
  name               = "c13-boudicca-schedule-role"
  assume_role_policy = data.aws_iam_policy_document.schedule_trust_policy.json

  inline_policy {
    name   = "c13-shayak-pharmazer-execution-policy"
    policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["ecs:RunTask"],
            "Resource": [replace(aws_ecs_task_definition.mp_article_analyser.arn, "/:\\d+$/", ":*")],
            "Condition": {"ArnLike": {"ecs:cluster": data.aws_ecs_cluster.c13_cluster.arn}}
        },
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": ["*"],
            "Condition": {"StringLike": {"iam:PassedToService": "ecs-tasks.amazonaws.com"}}
        }
      ]
    })
  }
}

resource "aws_security_group" "article_analyser_sg" {
    name   = "c13-boudicca-analyser-sg"
    vpc_id = data.aws_vpc.c13-vpc.id

    ingress = [
        {
            from_port        = 0
            to_port          = 0
            protocol         = "-1"
            cidr_blocks      = ["0.0.0.0/0"]
            description      = "Allow all inbound traffic"
            ipv6_cidr_blocks = []
            prefix_list_ids  = []
            security_groups  = []
            self             = false
        }
    ]

    egress = [
        {
            from_port        = 0
            to_port          = 0
            protocol         = "-1"
            cidr_blocks      = ["0.0.0.0/0"]
            description      = "Allow all outbound"
            ipv6_cidr_blocks = []
            prefix_list_ids  = []
            security_groups  = []
            self             = false
        }
    ]
}

resource "aws_cloudwatch_event_target" "ecs_target" {
  rule      = aws_cloudwatch_event_rule.csv_upload_to_s3_event_rule.name
  arn       = data.aws_ecs_cluster.c13_cluster.arn
  role_arn  = aws_iam_role.schedule_role.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.mp_article_analyser.arn
    launch_type         = "FARGATE"
    network_configuration {
      subnets         = [
          data.aws_subnet.c13-public-subnet1.id,
          data.aws_subnet.c13-public-subnet2.id,
          data.aws_subnet.c13-public-subnet3.id
      ]
      security_groups = [aws_security_group.article_analyser_sg.id] 
      assign_public_ip = true
    }
  }
}

# =========================== MP Dashboard ===========================

resource "tls_private_key" "private_key" {
    algorithm = "RSA"
    rsa_bits = 4096
}

resource "local_file" "private_key_file" {
    content  = tls_private_key.private_key.private_key_pem
    filename = "${path.module}/c13-boudicca-mp-key-pair.pem"
}

resource "aws_key_pair" "key_pair" {
    key_name = "c13-boudicca-mp-key-pair"
    public_key = tls_private_key.private_key.public_key_openssh
}

resource "aws_security_group" "ec2_sg" {
    name = "c13-boudicca-ec2-security-group"
    vpc_id = data.aws_vpc.c13-vpc.id
    ingress = [
        {
            from_port = 22
            to_port = 22
            protocol = "TCP"
            cidr_blocks = ["0.0.0.0/0"]
            description = "Allow ssh"
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = []
            self = false
        },
        {
            from_port   = 8501
            to_port     = 8501
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
            description = "Allow streamlit"
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = []
            self = false
        },
        {
            from_port   = 80
            to_port     = 80
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
            description = "Allow connection"
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = []
            self = false
        }
    ]
    egress = [
        {   
            from_port = 0
            to_port = 0
            protocol = "-1"
            cidr_blocks = ["0.0.0.0/0"]
            description = "Allow all outbound"
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = []
            self = false
        }
    ]
}

resource "aws_instance" "pipeline_ec2" {
    instance_type = "t3.micro"
    tags = {Name: "c13-boudicca-mp-dashboard"}
    security_groups = [aws_security_group.ec2_sg.id]
    subnet_id = data.aws_subnet.c13-public-subnet1.id
    associate_public_ip_address = true
    ami = "ami-0c0493bbac867d427"
    key_name = aws_key_pair.key_pair.key_name
    user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y python3
              EOF
    lifecycle {
      prevent_destroy = false
    }
}

resource "local_file" "instance_dns" {
  content  = "EC2_HOST=${aws_instance.pipeline_ec2.public_dns}"
  filename = "../dashboard/ec2.env"
}

# =========================== Emailing system ===========================

resource "aws_lambda_function" "daily_email_lambda" {
    function_name = "c13-boudicca-daily-email-lambda"
    image_uri     = data.aws_ecr_image.daily_email_image.image_uri
    role          = aws_iam_role.lambda_execution_role.arn
    package_type = "Image"
    timeout = 900
    memory_size = 256

    environment {
        variables = {
            S3_BUCKET_NAME = var.S3_BUCKET_NAME
            AWS_ACCESS_KEY_BOUDICCA = var.AWS_ACCESS_KEY
            AWS_ACCESS_SECRET_KEY_BOUDICCA = var.AWS_SECRET_ACCESS_KEY
            EC2_HOST = aws_instance.pipeline_ec2.public_dns
            DB_HOST = var.DB_HOST
            DB_PORT = var.DB_PORT
            DB_NAME = var.DB_NAME
            DB_USER = var.DB_USER
            DB_PASSWORD = var.DB_PASSWORD
            FROM_EMAIL = var.FROM_EMAIL
        }
    }

    image_config { command = ["daily_email.lambda_handler"] }
}

resource "aws_lambda_function" "weekly_email_lambda" {
    function_name = "c13-boudicca-weekly-email-lambda"
    image_uri     = data.aws_ecr_image.weekly_email_image.image_uri
    role          = aws_iam_role.lambda_execution_role.arn
    package_type = "Image"
    timeout = 900
    memory_size = 256

    environment {
        variables = {
            S3_BUCKET_NAME = var.S3_BUCKET_NAME
            AWS_ACCESS_KEY_BOUDICCA = var.AWS_ACCESS_KEY
            AWS_ACCESS_SECRET_KEY_BOUDICCA = var.AWS_SECRET_ACCESS_KEY
            DB_HOST = var.DB_HOST
            DB_PORT = var.DB_PORT
            DB_NAME = var.DB_NAME
            DB_USER = var.DB_USER
            DB_PASSWORD = var.DB_PASSWORD
            FROM_EMAIL = var.FROM_EMAIL
        }
    }

    image_config { command = ["weekly_email.lambda_handler"] }
}

data "aws_iam_policy_document" "eventbridge_schedule_trust_policy" {
    statement {
        effect = "Allow"
        principals {
            type        = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }
        actions = ["sts:AssumeRole"]
    }
}

resource "aws_iam_role" "eventbridge_scheduler_role" {
    name               = "c13-boudicca-email-eventbridge-scheduler-role"
    assume_role_policy = data.aws_iam_policy_document.eventbridge_schedule_trust_policy.json
}

resource "aws_iam_role_policy" "eventbridge_lambda_invocation_policy" {
    name = "EventBridgeLambdaInvocationPolicy"
    role = aws_iam_role.eventbridge_scheduler_role.id

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Effect = "Allow",
                Action = "lambda:InvokeFunction",
                Resource = [
                  aws_lambda_function.daily_email_lambda.arn,
                  aws_lambda_function.weekly_email_lambda.arn
                  ]
            },
            {
                Effect = "Allow",
                Action = "iam:PassRole",
                Resource = aws_iam_role.lambda_execution_role.arn
            }
        ]
    })
}

resource "aws_scheduler_schedule" "daily_email_schedule" {
    name        = "c13-boudicca-daily-email-schedule"
    description = "Scheduled rule to trigger the short-term ETL lambda every minute"
    schedule_expression = "cron(0 8 * * ? *)"

    flexible_time_window {
        mode = "OFF"
    }

    target {
        arn     = aws_lambda_function.daily_email_lambda.arn
        role_arn = aws_iam_role.eventbridge_scheduler_role.arn
    }
}

resource "aws_scheduler_schedule" "weekly_email_schedule" {
    name        = "c13-boudicca-weekly-email-schedule"
    description = "Scheduled rule to trigger the short-term ETL lambda every minute"
    schedule_expression = "cron(0 8 ? * 1 *)"

    flexible_time_window {
        mode = "OFF"
    }

    target {
        arn     = aws_lambda_function.weekly_email_lambda.arn
        role_arn = aws_iam_role.eventbridge_scheduler_role.arn
    }
}
