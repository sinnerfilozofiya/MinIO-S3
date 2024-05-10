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

# Expose port 5000 to the outside world
EXPOSE 5000

# Specify the command to run on container start
CMD ["gunicorn", "--workers", "3", "--bind", "127.0.0.1:7000", "-m", "007", "wsgi:app"]
