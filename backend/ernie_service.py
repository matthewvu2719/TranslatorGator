"""
ERNIE 0.3B–3B integration for manga translation using Hugging Face
"""
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
import torch
from typing import Optional

class ERNIETranslator:
    def __init__(self, model_name: str = "baidu/ERNIE-4.5-0.3B-PT"):
        print(f"[ERNIE] Loading model: {model_name}")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, 
            trust_remote_code=True,
            legacy=False
        )
        
        # Load model with trust_remote_code to handle custom architectures
        dtype = torch.float16 if self.device=="cuda" else torch.float32
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                dtype=dtype,
                device_map="auto" if self.device=="cuda" else None,
                low_cpu_mem_usage=True
            )
        except ValueError as e:
            print(f"[ERNIE] AutoModelForCausalLM failed: {e}")
            print("[ERNIE] Trying with AutoModel and trust_remote_code...")
            from transformers import AutoModel
            self.model = AutoModel.from_pretrained(
                model_name,
                trust_remote_code=True,
                dtype=dtype,
                device_map="auto" if self.device=="cuda" else None,
                low_cpu_mem_usage=True
            )
        
        self.model.eval()
        print("[ERNIE] Model loaded successfully!")

    def translate(self, text: str, mode: str = "natural") -> str:
        """
        Translate manga text
        """
        prompts = {
            "natural": f"Translate this Japanese manga text to natural English. Keep it short and conversational:\n{text}\n\nEnglish:",
            "literal": f"Translate literally:\n{text}\n\nEnglish:",
            "casual": f"Translate this manga dialogue casually with slang:\n{text}\n\nEnglish:",
            "polite": f"Translate formally:\n{text}\n\nEnglish:"
        }

        input_text = prompts.get(mode, prompts["natural"])

        try:
            inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=128,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            decoded = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
            return decoded.strip()
        except Exception as e:
            print(f"[ERNIE] Translation error: {e}")
            return text

# Singleton instance
_ernie_translator = None

def get_ernie_translator(model_name: str = "baidu/ERNIE-4.5-0.3B-PT") -> ERNIETranslator:
    global _ernie_translator
    if _ernie_translator is None:
        _ernie_translator = ERNIETranslator(model_name)
    return _ernie_translator
