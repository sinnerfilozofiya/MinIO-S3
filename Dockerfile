# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY Requirements.txt .

# Install the dependencies
RUN pip install -r Requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Specify the command to run on container start
#CMD ["python", "run.py"]
CMD ["gunicorn", "--workers", "3", "--bind", "unix:/var/www/sockets/minios3.sock", "-m", "007", "wsgi:app"]