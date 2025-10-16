import os
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

load_dotenv()

USE_DYNAMODB = os.getenv("USE_DYNAMODB", "false").lower() == "true"

if USE_DYNAMODB:
    # connect to DynamoDB
    dynamo = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION"))
    table = dynamo.Table(os.getenv("DYNAMODB_TABLE"))

# fallback to in-memory store for dev/demo
NOTES = {}

def save_note(username, title, encrypted_text):
    """Save a note for a user."""
    if USE_DYNAMODB:
        table.put_item(Item={
            'pk': f"{username}#{title}",  # composite key
            'content': encrypted_text
        })
    else:
        if username not in NOTES:
            NOTES[username] = {}
        NOTES[username][title] = encrypted_text

def get_note(username, title):
    """Retrieve a note for a user."""
    if USE_DYNAMODB:
        resp = table.get_item(Key={'pk': f"{username}#{title}"})
        item = resp.get("Item")
        return item.get("content") if item else None
    else:
        return NOTES.get(username, {}).get(title)

# s3 helpers

s3 = boto3.client("s3")

def upload_file_bytes(bucket, key, data_bytes):
    """
    Uploads raw bytes to an S3 bucket.
    Example usage:
        upload_file_bytes("my-bucket", "notes/user1/note1.txt", b"encrypted content")
    """
    s3.put_object(Bucket=bucket, Key=key, Body=data_bytes)