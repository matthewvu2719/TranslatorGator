"""
Script to pre-download ERNIE models from Hugging Face
Run this before starting the server to avoid delays
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
import sys

def download_model(model_name: str):
    """Download and cache ERNIE model"""
    print(f"Downloading {model_name}...")
    print("This may take a while depending on your internet speed.")
    
    try:
        print("Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        
        print("Downloading model weights...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        
        print(f"✓ Successfully downloaded {model_name}")
        print(f"Model cached at: ~/.cache/huggingface/hub/")
        return True
        
    except Exception as e:
        print(f"✗ Error downloading model: {e}")
        return False

if __name__ == "__main__":
    models = {
        "1": ("baidu/ERNIE-4.5-8B-Instruct", "Best quality (16GB VRAM)"),
        "2": ("baidu/ERNIE-4.5-3B-Instruct", "Balanced (6GB VRAM)"),
        "3": ("baidu/ERNIE-4.5-1.5B-Instruct", "Fastest (3GB VRAM)")
    }
    
    print("🐊 Translator Gator - Model Downloader")
    print("\nAvailable ERNIE models:")
    for key, (name, desc) in models.items():
        print(f"{key}. {name} - {desc}")
    
    choice = input("\nSelect model to download (1-3): ").strip()
    
    if choice in models:
        model_name, _ = models[choice]
        success = download_model(model_name)
        
        if success:
            print("\n✓ Model ready! You can now start the server.")
            print(f"  python main.py")
    else:
        print("Invalid choice!")
        sys.exit(1)
