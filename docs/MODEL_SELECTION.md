# ERNIE Model Selection Guide

## Available Models

All models are from Hugging Face: https://huggingface.co/collections/baidu/ernie-45

### 1. ERNIE-4.5-8B-Instruct (Recommended)
- **Size**: 8 billion parameters
- **VRAM**: ~16GB
- **Quality**: Best translation quality
- **Speed**: ~2-3 seconds per bubble
- **Use for**: Competition submission, demo video

### 2. ERNIE-4.5-3B-Instruct (Balanced)
- **Size**: 3 billion parameters
- **VRAM**: ~6GB
- **Quality**: Very good
- **Speed**: ~1-2 seconds per bubble
- **Use for**: Development, testing

### 3. ERNIE-4.5-1.5B-Instruct (Fast)
- **Size**: 1.5 billion parameters
- **VRAM**: ~3GB
- **Quality**: Good
- **Speed**: <1 second per bubble
- **Use for**: Quick testing, CPU-only systems

## Hardware Requirements

### GPU (Recommended)
- NVIDIA GPU with CUDA support
- 16GB VRAM for 8B model
- 6GB VRAM for 3B model
- 3GB VRAM for 1.5B model

### CPU Only (Slower)
- Works but 10-20x slower
- Use 1.5B model only
- 16GB+ RAM recommended

## Switching Models

Edit `backend/.env`:

```bash
# For best quality
ERNIE_MODEL=baidu/ERNIE-4.5-8B-Instruct

# For balanced performance
ERNIE_MODEL=baidu/ERNIE-4.5-3B-Instruct

# For speed/low memory
ERNIE_MODEL=baidu/ERNIE-4.5-1.5B-Instruct
```

Then restart the server.

## Why Hugging Face Instead of API?

✅ **Free**: No API costs or rate limits
✅ **Fast**: Local inference, no network latency
✅ **Private**: Your data stays on your machine
✅ **Customizable**: Can fine-tune the model
✅ **Competition-ready**: Required for model submission

## Fine-tuning for Competition

To win "Best ERNIE Fine-Tune" category:

1. Start with base model
2. Create manga translation dataset
3. Fine-tune using LLaMA-Factory or Unsloth
4. Upload to Hugging Face
5. Submit model URL

See `docs/FINETUNING.md` for details.
