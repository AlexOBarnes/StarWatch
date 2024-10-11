source .env
aws ecr get-login-password --region $AWS_REGION| docker login --username AWS --password-stdin $ECR_URI
docker build -t $IMAGE_NAME . --platform "linux/amd64"
docker tag $IMAGE_NAME:latest $ECR_URI:latest
docker push $ECR_URI:latest 