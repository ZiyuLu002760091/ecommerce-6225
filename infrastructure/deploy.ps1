# Set your AWS region and account ID
$AWS_REGION="us-east-1"
$AWS_ACCOUNT_ID = aws sts get-caller-identity --query Account --output text

# Create ECR repository if it doesn't exist
aws ecr describe-repositories --repository-names micro-ecommerce-backend
if ($LASTEXITCODE -ne 0) {
    aws ecr create-repository --repository-name micro-ecommerce-backend
}

# Build and push Docker image
Set-Location -Path ../micro-ecommerce
docker build -t micro-ecommerce-backend .
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
docker tag micro-ecommerce-backend:latest "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/micro-ecommerce-backend:latest"
docker push "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/micro-ecommerce-backend:latest"

# Deploy CloudFormation stack
Set-Location -Path ../infrastructure
aws cloudformation deploy `
    --template-file backend-infrastructure.yml `
    --stack-name micro-ecommerce-backend `
    --parameter-overrides `
        EnvironmentName=production `
        DBPassword=DevDB#123456789 `
        RabbitMQPassword=DevRMQ#123456789 `
    --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND