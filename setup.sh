#!/bin/bash

# Install Docker if not already installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Docker is not installed. Please install Docker and try again."
  exit 1
fi

# Build the Docker image and start the containers
docker-compose up --build -d

# Wait for the FastAPI application to start
sleep 10

# Check if the FastAPI application is running
if curl --fail http://localhost:8000/docs; then
  echo "FastAPI application is up and running at http://localhost:8000/docs"
else
  echo "Failed to start the FastAPI application."
fi
