# AWS Setup for SafeNote

## PreRequisites
* 1. AWS account with sufficient permissions
* 2. Domain pointing to your EC2 public IP
* 3. AWS CLI installed locally
* 4. SSH key pair for EC2 access
* 5. Python 3.9+, pip, and virtualenv

## EC2 Instance Setup
* Launch EC2 instance with Ubuntu 22.04 LTS
* Instance type: t2.micro (Free Tier)
* Key pair: use a .pem file to SSH
* Security group:
*   - SSH (22) from your IP only
*   - HTTP (80) and HTTPS (443) from anywhere
* Assign IAM role (see next section)

## IAM Role
* Create an IAM role for EC2 with minimal permissions
* Example policy:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/SafeNote"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::safenote-storage",
        "arn:aws:s3:::safenote-storage/*"
      ]
    }
  ]
}

## DynamoDB Setup
* Example CLI:
aws dynamodb create-table \
  --table-name SafeNote \
  --attribute-definitions AttributeName=pk,AttributeType=S \
  --key-schema AttributeName=pk,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region us-east-1

## S3 Bucket Setup
* Create bucket: safenote-storage
* Block all public access
* Enable SSE-S3 encryption
* EC2 IAM role allows PutObject/GetObject

## Install Nginx
# 1. Update packages
sudo apt update && sudo apt upgrade -y

# 2. Install Nginx
sudo apt install nginx -y

# 3. Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# 4. Run Certbot for the domain
sudo certbot --nginx -d safenoteapp.com -d www.safenoteapp.com

# 5. Verify certificate
sudo certbot certificates

# 6. Test HTTPS
curl -I https://safenoteapp.com

## Environment Variables
FLASK_ENV=production
SECRET_KEY=<your-jwt-secret>
ENCRYPTION_KEY=<your-encryption-key>
AWS_REGION=us-east-1
DYNAMODB_TABLE=SafeNote
S3_BUCKET=safenote-storage
DEBUG=False
