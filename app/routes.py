import os
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
    filename = request.form.get('filename', file.filename)  # Use provided filename or default to the uploaded file's name

    if filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        filename = secure_filename(filename)
        file_path = os.path.join('./', filename)  # Temporary save path
        file.save(file_path)

        if upload_to_aws(file_path, Bucket_name, filename):
            os.remove(file_path)  # Clean up the temporary file
            return jsonify({'message': 'File successfully uploaded'}), 200
        else:
            os.remove(file_path)  # Clean up the temporary file
            return jsonify({'error': 'Upload to AWS failed'}), 500

    return jsonify({'error': 'Invalid file or filename'}), 400