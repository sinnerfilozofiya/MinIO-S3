
import requests

def upload_file_to_api(api_url, file_path):
    with open(file_path, 'rb') as file:

        files = {'file': (file)}


        response = requests.post(api_url, files=files)
        return response

# Usage
api_url = 'http://127.0.0.1:6000/upload'
file_path = './acter.png'

response = upload_file_to_api(api_url, file_path)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")