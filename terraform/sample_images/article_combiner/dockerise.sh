source .env
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com
docker rmi $IMAGE_SHORT_TERM_NAME_PIPELINE
docker build -t $IMAGE_SHORT_TERM_NAME_PIPELINE . --platform "linux/amd64" 
docker tag $IMAGE_SHORT_TERM_NAME_PIPELINE:latest $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com/$ECR_SHORT_TERM_REPO_NAME:latest
docker push $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com/$ECR_SHORT_TERM_REPO_NAME:latest