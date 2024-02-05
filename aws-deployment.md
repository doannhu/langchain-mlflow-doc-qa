**Steps:**
1. Install AWS Cli: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html; check ver: aws --version

2. Authenticate local PowerShell: 
    - create access key with CloudShell, command aws iam create-access-key. more information: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey_CLIAPI
    - using access key in local PS: aws configure

3. Create repository in AWS ECR (Elastic Container Registry) - private mode and follow instruction from View Push Commands:
    - authenticate docker to allow push to ECR. template: aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
    - build local docker image docker build -t chainlit-langchain-demo .
    - tag image: docker tag chainlit-langchain-demo:latest 197142715819.dkr.ecr.ap-southeast-2.amazonaws.com/chainlit-langchain-demo:latest
    - push image from local docker to ecr: docker push 197142715819.dkr.ecr.ap-southeast-2.amazonaws.com/chainlit-langchain-demo:latest

4. Run container in AWS ECS (Elastic Container Service):
    - create Cluster (infrastructure: AWS Fargate - serverless)
    - create Task Definitions to connect to image on ECR (copy image URI) and set up AWS Fargate(OS Linux/x86_64, 1 CPU, 3GB RAM, create Port mappings Container port 8000, TCP Protocol, port name: Chainlit-tcp)
    - create Service in Cluster with above Task definition
    - open port 8000. Go to Service in Cluster/Configuration and networking/Network configuration/ Security groups and open that group. Edit Inbounce rules for that `Security group ID`: Custom TCP type, port range 8000

5. Access to app: Open running task in Task Definitions and go to `Public IP` in `Configuraion`. that is IP address