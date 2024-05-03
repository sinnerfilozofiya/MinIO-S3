import os
from app import s3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from mimetypes import guess_type

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../credentials/.env'))

def upload_to_aws(local_file, bucket_name, s3_file):
    
    # Guess the file content type
    content_type, _ = guess_type(local_file)

    try:
        # Upload the file with the appropriate content type
        s3.upload_file(local_file, bucket_name, s3_file, ExtraArgs={'ContentType': content_type or 'application/octet-stream','CacheControl': 'no-store, max-age=0'})
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
