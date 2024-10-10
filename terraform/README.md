# Cloud Deployment using Terraform

##  Prerequisites
- **Terraform** installed
- **ECR** repos for the following:
    - Fox news scraper image
    - Democracy now scraper image
    - Article analyser image
    - Email generator image
- Provision **PostgreSQL RDS** instance
- Read the following READMEs to setup containers, database and upload:
    1. news_sentiment_analyser/README.md
    2. fox_news_scraper/README.md
    3. democracy_now_scraper/RADME.md
    4. dashboard/README.md
    5. database/README.md


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

S3_BUCKET_NAME  = "name-of-S3-bucket"

FOX_NEWS_SCRAPER_ECR_REPO       ="ecr-repo-name-for-fox-news-scraper"
DEMOCARCY_NOW_SCRAPER_ECR_REPO  ="ecr-repo-name-for-democracy-now-news-scraper"
ARTICLE_ANALYSER_ECR_REPO       ="ecr-repo-name-for-article-analyser"
EMAIL_GENERATOR_ECR_REPO        ="ecr-repo-name-for-email-generator"

DB_HOST               = "your-RDS-host"
DB_PORT               = "your-RDS-port"
DB_NAME               = "your-RDS-name"
DB_USER               = "your-RDS-user"
DB_PASSWORD           = "your-RDS-password"

OPENAI_API_KEY          = "your-open-ai-key"
```
