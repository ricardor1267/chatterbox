#!/bin/bash

# Script to build and push Chatterbox RunPod Docker image
# Usage: ./build_worker.sh [your-dockerhub-username]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

DOCKER_USERNAME=${1:-"your-username"}
IMAGE_NAME="chatterbox-runpod-worker"
TAG="latest"

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Chatterbox RunPod Worker Builder${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

if [ "$DOCKER_USERNAME" = "your-username" ]; then
    echo -e "${RED}Error: Please provide your Docker Hub username${NC}"
    echo "Usage: ./build_worker.sh YOUR_DOCKERHUB_USERNAME"
    exit 1
fi

FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"

echo -e "${YELLOW}Building image:${NC} ${FULL_IMAGE_NAME}"
echo ""

# Build the image (must be linux/amd64 for RunPod)
docker build --platform linux/amd64 -t ${FULL_IMAGE_NAME} -f Dockerfile .

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Docker image built successfully!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Push to Docker Hub:"
    echo "   ${GREEN}docker push ${FULL_IMAGE_NAME}${NC}"
    echo ""
    echo "2. Test locally (optional):"
    echo "   ${GREEN}docker run --rm --gpus all ${FULL_IMAGE_NAME}${NC}"
    echo ""
    echo "3. Use in RunPod:"
    echo "   Template > Container Image: ${GREEN}${FULL_IMAGE_NAME}${NC}"
    echo ""
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi
