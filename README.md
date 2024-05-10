# MinIO-S3 Integration Project
This project aims to demonstrate the integration of MinIO, an open-source object storage server compatible with Amazon S3 API, with a Python Flask API for file uploads.


## Overview

MinIO is a high-performance, distributed object storage server designed for large-scale data infrastructure. It is API-compatible with Amazon S3, making it easy to integrate with existing S3-compatible applications and tools.

In this project, we explore how to set up a MinIO server using Docker and interact with it via a Python Flask API. The Flask API allows users to upload files to the MinIO server using the S3 API.

## Features
- MinIO Server: Dockerized MinIO server configured to run locally.
- Flask API: Python Flask API for handling file uploads to MinIO.
- Upload Functionality: Ability to upload files to the MinIO server via the Flask API.
- Customization: Option to specify custom filenames for uploaded files.

# How It Works
## Step 1: Filling the .env File

first fill the related credentials in the relative path:
credentials\.env
- `MINIO_ENDPOINT_URL`: this is the your host IP.
- `MINIO_ACCESS_KEY_ID`: get this from MinIO MinIO/Access Keys.
- `MINIO_SECRET_ACCESS_KEY`: get this from MinIO MinIO/Access Keys.
- `MINIO_S3_BUCKET_NAME`: name of the bucket you created at MinIO.



## Step 2: Create the docker containers

```sh
docker-compose --env-file credentials/.env up

```
## Step 3: add the following Policy as new role to make the buckets public  
```JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::*/*"
            ]
        }
    ]
}
```

## Step 4: Create Access Keys and copy them into [env](./credentials/.env) file


## Step 5: Create a bucket and make the Access Policy to public and add the name into the [env](./credentials/.env) file


## Step 6: Rebuild the docker-compose file 
```sh
docker-compose --env-file credentials/.env up

```
# File end-points
```sh
http://<minio-server>:9000/<bucket-name>/<file-name>
```
# how to deploy

## step 1: set the required permissions
```sh
sudo chmod 755 /var/www/sockets
```
```sh
sudo chown www-data:www-data /var/www/sockets/minios3.sock
```

## step 2: configure NGINX for both MinIO and RADOS gateway

```conf
erver {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://unix:/var/www/sockets/GateWay.sock;  # Path to the Gunicorn Unix socket
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }
}

```

## API Endpoint

**POST /upload**

## Base URL

```
https://your.domain.address
```


## Endpoint Description

This endpoint is designed for uploading files to an MinIO S3 bucket. It requires a file part in the request and optionally accepts a custom filename.

## Request Parameters

- `file`: File to be uploaded (required).
- `filename`: Custom filename for the file (optional).

## Responses

- `200 OK`: File successfully uploaded.
- `400 Bad Request`: Missing file part in the request or no file selected.
- `500 Internal Server Error`: Upload to AWS failed.

## Example Usage Of API 

### Python

```python
import requests

def upload_file_to_api(api_url, file_path, custom_filename=None):
    with open(file_path, 'rb') as file:
        filename = custom_filename if custom_filename else file.name
        files = {'file': (filename, file)}
        data = {'filename': filename}

        response = requests.post(api_url, files=files, data=data)
        return response

# Usage
api_url = 'https://your.domain.address/upload'
file_path = './photo.png'
custom_filename = 'xxxxxx.png'

response = upload_file_to_api(api_url, file_path, custom_filename)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

### Javascript
```javascript
const fs = require('fs');
const axios = require('axios');
const FormData = require('form-data');

async function uploadFileToApi(apiUrl, filePath, customFilename = null) {
    const form = new FormData();
    const filename = customFilename || filePath.split('/').pop();
    form.append('file', fs.createReadStream(filePath), filename);
    form.append('filename', filename);

    try {
        const response = await axios.post(apiUrl, form, {
            headers: {
                ...form.getHeaders()
            }
        });
        return response.data;
    } catch (error) {
        return error.response.data;
    }
}

// Usage
const apiUrl = 'https://your.domain.address/upload';
const filePath = './photo.png';
const customFilename = 'xxxxxx.png';

uploadFileToApi(apiUrl, filePath, customFilename)
    .then(data => console.log(data))
    .catch(err => console.error(err));

```