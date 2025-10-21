# Use NVIDIA CUDA base image with Python
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CUDA_HOME=/usr/local/cuda \
    PATH=${CUDA_HOME}/bin:${PATH} \
    LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-dev \
    git \
    wget \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Set working directory
WORKDIR /

# Copy project files
COPY pyproject.toml /
COPY src /src

# Install Chatterbox and dependencies
RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir runpod

# Copy the handler
COPY rp_handler.py /rp_handler.py

# Pre-download models to speed up cold starts
# This downloads models during build time (optional but recommended)
RUN echo "Downloading models..." && \
    python3 -c "from chatterbox.mtl_tts import ChatterboxMultilingualTTS; ChatterboxMultilingualTTS.from_pretrained(device='cpu')" || true

# Set the handler as the entrypoint
CMD ["python3", "-u", "/rp_handler.py"]
