# Docker Setup Guide

Docker makes deployment easy and ensures consistent environments across machines.

## Quick Start

### CPU-Only (Slower, but works everywhere)

```bash
# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

### GPU-Enabled (Recommended for best performance)

**Prerequisites:**
- NVIDIA GPU
- NVIDIA Docker runtime installed

```bash
# Build and start with GPU
docker-compose -f docker-compose.gpu.yml up -d

# Check logs
docker-compose -f docker-compose.gpu.yml logs -f

# Stop
docker-compose -f docker-compose.gpu.yml down
```

## Install NVIDIA Docker (for GPU support)

### Ubuntu/Debian
```bash
# Add NVIDIA Docker repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### Windows (WSL2)
1. Install Docker Desktop with WSL2 backend
2. Install NVIDIA drivers for Windows
3. Enable GPU support in Docker Desktop settings

## Configuration

### Choose Model Size

Edit `docker-compose.yml` or `docker-compose.gpu.yml`:

```yaml
environment:
  # For CPU or low VRAM
  - ERNIE_MODEL=baidu/ERNIE-4.5-1.5B-Instruct
  
  # For balanced (6GB VRAM)
  - ERNIE_MODEL=baidu/ERNIE-4.5-3B-Instruct
  
  # For best quality (16GB VRAM)
  - ERNIE_MODEL=baidu/ERNIE-4.5-8B-Instruct
```

### Add Hugging Face Token (Optional)

For private models or faster downloads:

```bash
# Create .env file
echo "HUGGINGFACE_TOKEN=hf_your_token_here" > .env

# Docker Compose will automatically load it
```

## Model Caching

Models are cached in a Docker volume to avoid re-downloading:

```bash
# View cached models
docker volume inspect translator-gator_huggingface-cache

# Clear cache (forces re-download)
docker volume rm translator-gator_huggingface-cache
```

## Development Mode

The docker-compose files mount your code directory, so changes are reflected immediately:

```bash
# Edit code in backend/
# Restart container to apply changes
docker-compose restart
```

## Production Deployment

### Build optimized image

```bash
# Build without dev mounts
docker build -t translator-gator:latest ./backend

# Run
docker run -d \
  -p 8000:8000 \
  -e ERNIE_MODEL=baidu/ERNIE-4.5-3B-Instruct \
  --name translator-gator \
  translator-gator:latest
```

### Deploy to cloud

The Docker image works on:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform
- Any Kubernetes cluster

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Check if port is in use
netstat -an | grep 8000
```

### Out of memory
```bash
# Use smaller model
ERNIE_MODEL=baidu/ERNIE-4.5-1.5B-Instruct docker-compose up
```

### GPU not detected
```bash
# Test GPU access
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Slow first startup
First run downloads the model (~3-15GB depending on size). This is normal and only happens once.

## Health Check

```bash
# Check if API is ready
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","ernie_loaded":true,"ocr_loaded":true}
```

## Performance Tips

1. **Use GPU**: 10-20x faster than CPU
2. **Use smaller model for dev**: 1.5B model for testing, 8B for demo
3. **Increase Docker memory**: Docker Desktop → Settings → Resources
4. **Use SSD**: Faster model loading from cache

## For Competition Demo

Use GPU docker-compose for best quality:

```bash
# Start with best model
docker-compose -f docker-compose.gpu.yml up -d

# Wait for model to load (check logs)
docker-compose -f docker-compose.gpu.yml logs -f

# Test translation
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com/manga.jpg","mode":"natural"}'
```
