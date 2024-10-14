# Cloud Deployment using Terraform

The project is designed to be deployed on the cloud using AWS services via terraform. Assuming some prerequisite setup explained int this document, the cloud infrastructure can be deployed using a single command.

##  Prerequisites
- **Terraform** installed
- **AWS ECR** repositories for the following:
    - Fox news scraper image
    - Democracy now scraper image
    - Article analyser image
    - Daily email image
    - Weekly email image
- Provision an **AWS RDS (PostgreSQL)** instance
- Provision a **AWS S3**
- Read the Prequrequisites and Setup section of the following READMEs (setup and upload images to ECR repositories):
    1. [news_sentiment_analyser/README.md](../news_sentiment_analyser/README.md)
    2. [fox_news_scraper/README.md](../fox_news_scraper/README.md)
    3. [democracy_now_scraper/README.md](../democracy_now_scraper/README.md)
    4. [daily-emailing/README.md](../daily-emailing/README.md)
    5. [weekly-emailing/README.md](../weekly-emailing/README.md)
- Read [database/README.md](../database/README.md) to initalise the database

##  Setup

1. Create `terraform.tfvars` file and fill with the following variables
    ```bash
    AWS_ACCESS_KEY        = "your-aws-access-key"
    AWS_SECRET_ACCESS_KEY = "your-aws-secret-key"

    REGION                = "your-region"
    VPC_ID                = "your-vpc-id"
    SUBNET_ID1            = "your-first-subnet-id"
    SUBNET_ID2            = "your-second-subnet-id"
    SUBNET_ID3            = "your-third-subnet-id"
    ECS_CLUSTER_NAME      = "your-aws-ecs-cluster-name"

    S3_BUCKET_NAME  = "name-of-S3-bucket"

    FOX_NEWS_SCRAPER_ECR_REPO       ="ecr-repo-name-for-fox-news-scraper"
    DEMOCARCY_NOW_SCRAPER_ECR_REPO  ="ecr-repo-name-for-democracy-now-news-scraper"
    ARTICLE_ANALYSER_ECR_REPO       ="ecr-repo-name-for-article-analyser"
    DAILY_EMAIL_ECR_REPO        ="ecr-repo-name-for-daily-emailer"
    WEEKLY_EMAIL_ECR_REPO        ="ecr-repo-name-for-weekly-emailer"

    DB_HOST               = "your-RDS-host"
    DB_PORT               = "your-RDS-port"
    DB_NAME               = "your-RDS-name"
    DB_USER               = "your-RDS-user"
    DB_PASSWORD           = "your-RDS-password"

    OPENAI_API_KEY        = "your-open-ai-key"

    FROM_EMAIL            = "address-to-send-emails-from"
    ```

2. Initialise terraform:
    ```bash
    terraform init
    ```

3. Deploy cloud services:
    ```bash
    terraform apply
    ```
    - Enter yes when it asks to approve changes.
    - Can be used to redeploy if resource definitions have been changed.
    - Keep note of the `EC2_public_dns` output for step 4.
    
4. Transfer dashboard to EC2 by reading [dashboard/README.md](../dashboard/README.md)

5. To bring down the cloud infrastructure:
    ```bash
    terraform destroy
    ```
    - To recreate start again from step 3.

##  Notes

- Remember to add any `*.env` or `*.tfvars` files to gitignore if note already listed.
- Each time the `terraform apply` is run, the EC2 will be recreated with a new dns address meaning the [dashboard setup](../dashboard/README.md) will need top be redone each time.

