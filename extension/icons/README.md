# Extension Icons

## Quick Fix: Use Emoji as Icon

Since Python/PIL isn't available, here's the fastest solution:

### Option 1: Use online converter
1. Go to https://www.favicon-generator.org/
2. Upload any green alligator image or the SVG file
3. Download the generated icons
4. Rename them to icon16.png, icon48.png, icon128.png

### Option 2: Use the generated image
The AI-generated alligator is at:
https://mcp-tools-z-image-turbo.hf.space/--replicas/gf97b/gradio_api/file=/tmp/gradio/3ec9515513072c71d36900d8a47b354554ab668f55ab5587b4385c7d05681aa1/image.webp

1. Download it
2. Use an online image resizer (like https://www.iloveimg.com/resize-image)
3. Create 16x16, 48x48, and 128x128 versions
4. Save as PNG

### Option 3: Simple colored squares (temporary)
Create three simple green PNG files with any image editor or use this PowerShell:

```powershell
# This creates simple 1-pixel images that Chrome will accept
[System.IO.File]::WriteAllBytes("icon16.png", [byte[]](0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A))
[System.IO.File]::WriteAllBytes("icon48.png", [byte[]](0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A))
[System.IO.File]::WriteAllBytes("icon128.png", [byte[]](0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A))
```

## The AI Generated Image

I created a cute alligator using Hugging Face Z-Image model. Download it from the URL above and resize to create your icons!
