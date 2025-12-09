# Setup Guide

## Prerequisites

- Python 3.8+
- Chrome browser
- GPU recommended (16GB VRAM for best model, 3GB minimum)
- 20GB free disk space for models

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Download ERNIE Model

Run the model downloader:

```bash
python download_models.py
```

Choose model based on your hardware:
- **8B model**: Best quality (needs 16GB VRAM)
- **3B model**: Balanced (needs 6GB VRAM)  
- **1.5B model**: Fastest (needs 3GB VRAM)

This downloads the model from Hugging Face (no API key needed!).

### 3. Configure Environment (Optional)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit to change model size if needed:

```
ERNIE_MODEL=baidu/ERNIE-4.5-3B-Instruct
```

### 4. Run Backend

```bash
python main.py
```

First startup takes 1-2 minutes to load the model.

Server runs at: http://localhost:8000

Check health: http://localhost:8000/health

## Extension Setup

### 1. Load Extension in Chrome

1. Open Chrome
2. Go to `chrome://extensions/`
3. Enable "Developer mode" (top right)
4. Click "Load unpacked"
5. Select the `extension` folder

### 2. Test Extension

1. Visit any manga website (e.g., mangadex.org)
2. Click the Translator Gator icon
3. Select translation mode
4. Click "Translate Page"

## Development

### Backend Development

```bash
# Install dev dependencies
pip install pytest black flake8

# Run tests
pytest

# Format code
black .
```

### Extension Development

1. Make changes to extension files
2. Go to `chrome://extensions/`
3. Click reload icon on Translator Gator
4. Test changes

## Troubleshooting

### Backend won't start
- Check Python version: `python --version`
- Verify dependencies: `pip list`
- Check port 8000 is free

### Extension not working
- Check backend is running
- Open browser console (F12)
- Look for CORS errors
- Verify API URL in `content.js`

### OCR not detecting text
- Check image quality
- Verify PaddleOCR installation
- Try different manga pages
- Check console logs

### Translation errors
- Verify ERNIE API key
- Check API quota/limits
- Review error messages in backend logs

## API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
