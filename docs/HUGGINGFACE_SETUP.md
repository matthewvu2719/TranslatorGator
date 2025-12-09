# Hugging Face MCP Setup

The Hugging Face MCP server is configured for easy model access and deployment.

## Setup Steps

### 1. Install UV (if not already installed)

**Windows:**
```bash
pip install uv
```

Or visit: https://docs.astral.sh/uv/getting-started/installation/

### 2. Get Hugging Face API Key

1. Go to https://huggingface.co/settings/tokens
2. Create a new token with "write" access
3. Copy the token

### 3. Configure MCP

Edit `.kiro/settings/mcp.json` and add your API key:

```json
{
  "mcpServers": {
    "huggingface": {
      "command": "uvx",
      "args": ["mcp-server-huggingface"],
      "env": {
        "HUGGINGFACE_API_KEY": "hf_your_actual_token_here"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### 4. Restart Kiro or Reconnect MCP

- Open Command Palette
- Search "MCP"
- Click "Reconnect MCP Servers"

## What You Can Do

With Hugging Face MCP, you can:

- **Upload fine-tuned models**: Push your ERNIE/PaddleOCR fine-tunes
- **Download models**: Pull pre-trained models for testing
- **Manage datasets**: Upload training data
- **Create model cards**: Document your models
- **Share with community**: Make models public for competition

## For Translator Gator

Use Hugging Face to:

1. **Host fine-tuned ERNIE model** (required for competition)
2. **Host fine-tuned PaddleOCR-VL** (for bubble detection)
3. **Share training datasets** (manga bubble annotations)
4. **Create model cards** (documentation for judges)

## Example: Upload Fine-tuned Model

Once MCP is connected, you can use Kiro to:
- Upload model weights to Hugging Face
- Create model repository
- Generate model cards
- Manage versions

This is required for the competition submission!
