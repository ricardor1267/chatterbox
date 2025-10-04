#!/bin/bash

# Script to build and push Chatterbox RunPod Docker image
# Usage: ./build.sh [your-dockerhub-username]

set -e

DOCKER_USERNAME=${1:-"your-username"}
IMAGE_NAME="chatterbox-runpod"
TAG="latest"

echo "Building Docker image: ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"

# Build the image (must be linux/amd64 for RunPod)
docker build --platform linux/amd64 -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG} -f .runpod/Dockerfile .

echo "Docker image built successfully!"
echo ""
echo "To push to Docker Hub, run:"
echo "  docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"
echo ""
echo "Then use this image in RunPod:"
echo "  ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"
