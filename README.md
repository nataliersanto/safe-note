# SafeNote

## About The Project

This project was created because I wanted to get familiar with cybersecurity tools, including **Suricata** and **Wireshark**, while building a secure note-taking application.  

SafeNote allows users to securely register, login, create, and retrieve encrypted notes stored in AWS DynamoDB. Passwords are hashed with bcrypt, notes are encrypted with AES-256, and authentication is handled with JWT tokens.  

> **Note:** As of right now, the frontend is not implemented at www.safenoteapp.com. The API is fully functional and can be tested using tools like **curl** or **Postman**.

The project also includes an **AWS setup guide** to deploy the backend securely.  


## Built With

- Python 3
- Flask
- Flask-JWT-Extended
- Flask-CORS
- boto3 (AWS SDK for Python)
- passlib (bcrypt)
- cryptography (Fernet / AES-256)
- Suricata (network traffic monitoring)  
- Wireshark (packet analysis)
- AWS S3, EC2, DynamoDb

## Getting Started

Follow these steps to get a local copy running on your machine.  

### Prerequisites

- Python 3.12+  
- pip (Python package manager)  
- Virtual environment (`venv`) recommended  
- AWS credentials configured if using DynamoDB/S3

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/safenote.git
cd safenote
```
2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Create a .env file with the following variables:
   
```bash
AWS_REGION=your-aws-region
USERS_TABLE=your-users-table
DYNAMODB_TABLE=your-notes-table
S3_BUCKET=your-s3-bucket
SECRET_KEY=your-jwt-secret
```
6. Run the flask app:

```bash
python3 app.py
```

## Usage

1. Register a User

```bash
curl -X POST http://127.0.0.1:5000/register \
-H "Content-Type: application/json" \
-d '{"username": "alice", "password": "MySecurePass123"}'
```
3. Login

```bash
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "alice", "password": "MySecurePass123"}'
```
You'll get a JSON response with an access_token. Use it in Bearer authorization for subsequent requests.

5. Create a Note

```bash
curl -X POST http://127.0.0.1:5000/notes \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{"title": "MyFirstNote", "content": "This is a secret note."}'
```
7. Retrieve a Note

```bash
curl -X GET http://127.0.0.1:5000/notes/MyFirstNote \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Contact

Natalie Santo - natalierosesanto@gmail.com

# Usage

## Wireshark capture showing SYN packets from a local host to a remote IP — used to analyze connection attempts detected by Suricata.

<img width="3024" height="1964" alt="Wireshark example edited" src="https://github.com/user-attachments/assets/5dd29a7f-8e89-447c-a384-04f72be7e037" />



## Examples of CURL requests

<img width="3016" height="532" alt="CURL example - Edited" src="https://github.com/user-attachments/assets/cc8e4653-7174-43b4-a987-7b62100f2413" />

