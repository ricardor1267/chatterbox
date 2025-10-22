#!/bin/bash

# Script to build and push Chatterbox RunPod Docker image
# Usage: ./build_worker.sh [your-dockerhub-username] [dockerfile-variant]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

DOCKER_USERNAME=${1:-"your-username"}
DOCKERFILE_VARIANT=${2:-"simple"}  # Options: simple, flexible, main
IMAGE_NAME="chatterbox-runpod-worker"
TAG="latest"

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Chatterbox RunPod Worker Builder${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

if [ "$DOCKER_USERNAME" = "your-username" ]; then
    echo -e "${RED}Error: Please provide your Docker Hub username${NC}"
    echo "Usage: ./build_worker.sh YOUR_DOCKERHUB_USERNAME [dockerfile-variant]"
    echo ""
    echo "Dockerfile variants:"
    echo "  simple   - Uses pip install chatterbox-tts (recommended, fastest)"
    echo "  flexible - Builds from source with flexible dependencies"
    echo "  main     - Standard build from source"
    exit 1
fi

# Select Dockerfile
case "$DOCKERFILE_VARIANT" in
    "simple")
        DOCKERFILE="Dockerfile.simple"
        echo -e "${BLUE}Using simple Dockerfile (pip install)${NC}"
        ;;
    "flexible")
        DOCKERFILE="Dockerfile.flexible"
        echo -e "${BLUE}Using flexible Dockerfile (build from source, flexible deps)${NC}"
        ;;
    "main")
        DOCKERFILE="Dockerfile"
        echo -e "${BLUE}Using main Dockerfile (build from source)${NC}"
        ;;
    *)
        echo -e "${RED}Error: Unknown dockerfile variant: $DOCKERFILE_VARIANT${NC}"
        echo "Valid options: simple, flexible, main"
        exit 1
        ;;
esac

# Check if Dockerfile exists
if [ ! -f "$DOCKERFILE" ]; then
    echo -e "${RED}Error: $DOCKERFILE not found${NC}"
    exit 1
fi

FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"

echo -e "${YELLOW}Building image:${NC} ${FULL_IMAGE_NAME}"
echo -e "${YELLOW}Using:${NC} ${DOCKERFILE}"
echo ""

# Build the image (must be linux/amd64 for RunPod)
echo -e "${BLUE}Building Docker image...${NC}"
docker build --platform linux/amd64 -t ${FULL_IMAGE_NAME} -f ${DOCKERFILE} .

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Docker image built successfully!${NC}"
    echo ""
    echo -e "${YELLOW}Image size:${NC}"
    docker images ${FULL_IMAGE_NAME} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo ""
    echo "1. Test locally (optional):"
    echo "   ${GREEN}docker run --rm ${FULL_IMAGE_NAME} python3 -c 'import runpod; print(\"RunPod OK\")'${NC}"
    echo ""
    echo "2. Push to Docker Hub:"
    echo "   ${GREEN}docker push ${FULL_IMAGE_NAME}${NC}"
    echo ""
    echo "3. Use in RunPod:"
    echo "   Template > Container Image: ${GREEN}${FULL_IMAGE_NAME}${NC}"
    echo ""
else
    echo -e "${RED}✗ Build failed${NC}"
    echo ""
    echo -e "${YELLOW}Troubleshooting tips:${NC}"
    echo "1. Try a different dockerfile variant:"
    echo "   ${GREEN}./build_worker.sh ${DOCKER_USERNAME} simple${NC}"
    echo ""
    echo "2. Check Docker daemon is running"
    echo "3. Ensure you have enough disk space (need ~20GB)"
    echo "4. Review error messages above"
    exit 1
fi
