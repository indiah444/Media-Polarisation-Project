source .env
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com
docker rmi $IMAGE_NAME
docker rmi $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com/$ECR_REPO_NAME:latest
docker build -t $IMAGE_NAME . --platform "linux/amd64" 
docker tag $IMAGE_NAME:latest $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com/$ECR_REPO_NAME:latest
docker push $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com/$ECR_REPO_NAME:latest