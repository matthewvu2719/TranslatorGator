"""
Pre-download ERNIE models from Hugging Face
"""
from transformers import AutoTokenizer, AutoModelForCausalLM

def download_model(model_name: str):
    print(f"[Downloader] Downloading {model_name}...")
    AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
    print(f"[Downloader] {model_name} downloaded successfully!")

if __name__ == "__main__":
    models = {
        "1": ("baidu/ERNIE-4.5-0.3B-PT", "Lightweight, CPU/GPU friendly"),
        "2": ("baidu/ERNIE-4.5-3B-PT", "Balanced quality, GPU recommended")
    }

    print("Available ERNIE models:")
    for k,v in models.items():
        print(f"{k}. {v[0]} - {v[1]}")

    choice = input("Select model to download (1-2): ").strip()
    if choice in models:
        download_model(models[choice][0])
    else:
        print("Invalid choice")
