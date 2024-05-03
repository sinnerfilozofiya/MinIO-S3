import os
import uuid
from app import app
from app import Bucket_name
from flask import request, jsonify
from app.s3_models import upload_to_aws
from werkzeug.utils import secure_filename


# Uploading File to S3-Bucket
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file:

        # Generate a UUID for the file
        uuid_val = uuid.uuid4()
        short_uuid = str(uuid_val)[:8]

        # Get the original filename and extract the file extension
        original_filename = secure_filename(file.filename)
        _, file_extension = os.path.splitext(original_filename)

        # Create a filename with the generated UUID and original file extension
        filename = f"{short_uuid}{file_extension}"
        file_path = os.path.join('/tmp', filename)  # Temporary save path
        file.save(file_path)

        if upload_to_aws(file_path, Bucket_name, filename):
            os.remove(file_path)  # Clean up the temporary file
            return jsonify({'message': 'File successfully uploaded', 'uuid': filename}), 200
        else:
            os.remove(file_path)  # Clean up the temporary file
            return jsonify({'error': 'Upload to MinIO failed'}), 500

    return jsonify({'error': 'Invalid file or filename'}), 400
