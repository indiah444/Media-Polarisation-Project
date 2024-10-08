# Prerequisites

# Setup

1. Create `terraform.tfvars` file and fill with the following variables
```bash
AWS_ACCESS_KEY        = "your-aws-access-key"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-key"

REGION                = "your-region"
VPC_ID                = "your-vpc-id"
SUBNET_ID1            = "your-first-subnet-id"
SUBNET_ID2            = "your-second-subnet-id"
SUBNET_ID3            = "your-third-subnet-id"

DB_HOST               = "your-RDS-host"
DB_PORT               = "your-RDS-port"
DB_NAME               = "your-RDS-name"
DB_USER               = "your-RDS-user"
DB_PASSWORD           = "your-RDS-password"

ECR_SHORT_TERM_REPO_NAME  =  "name-of-repo-to-store-short-term-etl-image"
ECR_LONG_TERM_REPO_NAME   =  "name-of-repo-to-store-long-term-etl-image"
```
