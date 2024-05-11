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



ENV FLASK_APP=run.py
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "7000"]
