# ☁️ Cloud Deployment using Terraform

The project is designed to be deployed on the cloud using AWS services via terraform. Assuming some prerequisite setup explained int this document, the cloud infrastructure can be deployed using a single command.

## 🛠️ Prerequisites
- **Terraform** installed
- **AWS CLI** downloaded
- **AWS ECR** repositories for the following:
    - Fox news scraper image
    - Democracy now scraper image
    - Article analyser image
    - Daily email image
    - Weekly email image
- Provision an **AWS RDS (PostgreSQL)** instance to host database
- Provision an **AWS S3** bucket
- Read the Prequrequisites and Setup section of the following READMEs (setup and upload images to ECR repositories):
    1. [news_sentiment_analyser/README.md](../news_sentiment_analyser/README.md)
    2. [fox_news_scraper/README.md](../fox_news_scraper/README.md)
    3. [democracy_now_scraper/README.md](../democracy_now_scraper/README.md)
    4. [daily-emailing/README.md](../daily-emailing/README.md)
    5. [weekly-emailing/README.md](../weekly-emailing/README.md)
- Read [database/README.md](../database/README.md) to initalise the database

## ⚙️ Setup
1. Install AWS CLI for your machine by following the link: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html and run the command:
    ```bash
    aws configure
    ```
    Follow the prompts to enter your AWS credentials.

2. Create `terraform.tfvars` file and fill with the following variables
    ```bash
    # AWS Credentials
    AWS_ACCESS_KEY        = "your-aws-access-key"
    AWS_SECRET_ACCESS_KEY = "your-aws-secret-key"

    # AWS Region and Network Config
    REGION                = "the-aws-region"
    VPC_ID                = "the-vpc-id"
    SUBNET_ID1            = "the-first-subnet-id"
    SUBNET_ID2            = "the-second-subnet-id"
    SUBNET_ID3            = "the-third-subnet-id"
    ECS_CLUSTER_NAME      = "the-aws-ecs-cluster-name"

    # S3 Bucket Name
    S3_BUCKET_NAME        = "name-of-S3-bucket"

    # ECR Repositories
    FOX_NEWS_SCRAPER_ECR_REPO       = "ecr-repo-name-for-fox-news-scraper"
    DEMOCRACY_NOW_SCRAPER_ECR_REPO  = "ecr-repo-name-for-democracy-now-news-scraper"
    ARTICLE_ANALYSER_ECR_REPO       = "ecr-repo-name-for-article-analyser"
    DAILY_EMAIL_ECR_REPO            = "ecr-repo-name-for-daily-emailer"
    WEEKLY_EMAIL_ECR_REPO           = "ecr-repo-name-for-weekly-emailer"

    # RDS Database Config
    DB_HOST               = "the-RDS-host-address"
    DB_PORT               = "the-RDS-port-number"
    DB_NAME               = "the-RDS-name"
    DB_USER               = "the-RDS-username"
    DB_PASSWORD           = "the-RDS-password"

    # OpenAI API configuration
    OPENAI_API_KEY        = "your-open-ai-key"

    # Email Configuration
    FROM_EMAIL            = "address-to-send-emails-from"
    ```

3. Initialise terraform:
    ```bash
    terraform init
    ```

4. Deploy cloud services:
    ```bash
    terraform apply
    ```
    - Enter yes when it asks to approve changes.
    - Can be used to redeploy if resource definitions have been changed.

5. Restrict the .pem key access:
    ```bash
    chmod 400 c13-boudicca-mp-key-pair.pem
    ```
    This is required for the pem key to actually work when connecting to EC2 via ssh.
    
6. Transfer dashboard to EC2 by reading [dashboard/README.md](../dashboard/README.md)

7. To bring down the cloud infrastructure:
    ```bash
    terraform destroy
    ```
    - To recreate start again from step 3.

## 📝 Notes

- Remember to add any `*.env`, `*.tfvars`, `*.pem`, `*.pemkey` files to gitignore if note already listed.
- Each time the `terraform apply` is run, the EC2 will be recreated with a new dns address meaning the [dashboard setup](../dashboard/README.md) will need top be redone each time.

