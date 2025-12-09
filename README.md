# Translator Gator 🐊

A Chrome extension that automatically translates manga and comics using PaddleOCR-VL and ERNIE AI.

## Features

- 🎯 Automatic speech bubble detection
- 🌐 Real-time translation with ERNIE 4.5/5
- 🎨 Clean text overlay on original artwork
- 📖 Support for vertical Japanese text
- 🔄 Multiple translation styles (literal, natural, casual)

## Architecture

```
Chrome Extension (Frontend)
    ↓
FastAPI Backend
    ↓
PaddleOCR-VL → ERNIE Translation → Canvas Overlay
```

## Competition Categories

- ✅ Best ERNIE Multimodal Application
- ✅ Best PaddleOCR-VL Application/Fine-tune
- ✅ Best Agent System (optional)
- ✅ Warm-up Task

## Quick Start

### Option 1: Docker (Recommended)
```bash
# CPU version
docker-compose up -d

# GPU version (faster)
docker-compose -f docker-compose.gpu.yml up -d
```

### Option 2: Local Python
```bash
cd backend
pip install -r requirements.txt
python download_models.py
python main.py
```

### Extension Setup
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` folder

See [docs/DOCKER.md](docs/DOCKER.md) for detailed Docker setup.

## Tech Stack

- **Frontend**: Chrome Extension (Manifest V3)
- **Backend**: FastAPI + Python
- **Models**: PaddleOCR-VL, ERNIE 4.5
- **Overlay**: HTML5 Canvas

## License

MIT
