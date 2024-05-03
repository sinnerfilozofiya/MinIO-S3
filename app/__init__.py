import os
import boto3
from flask import Flask
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../credentials/.env'))

# Set up MinIO endpoint URL and credentials
endpoint_url = os.getenv('MINIO_ENDPOINT_URL')
access_key = os.getenv('MINIO_ACCESS_KEY_ID')
secret_key = os.getenv('MINIO_SECRET_ACCESS_KEY')
Bucket_name = os.getenv('MINIO_S3_BUCKET_NAME')

# Create an S3 client
s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key)

from app import routes