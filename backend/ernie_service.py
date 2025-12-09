"""
ERNIE 4.5 integration for manga translation using Hugging Face models
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Optional

class ERNIETranslator:
    def __init__(self, model_name: str = "baidu/ERNIE-4.5-8B-Instruct"):
        """
        Initialize ERNIE translator with Hugging Face model
        
        Available ERNIE models:
        - baidu/ERNIE-4.5-8B-Instruct (recommended)
        - baidu/ERNIE-4.5-3B-Instruct (faster, less memory)
        - baidu/ERNIE-4.5-1.5B-Instruct (lightweight)
        """
        print(f"Loading ERNIE model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.model.eval()
        print("ERNIE model loaded successfully!")
    
    def translate(self, text: str, mode: str = "natural") -> str:
        """
        Translate manga text using ERNIE
        
        Args:
            text: Original Japanese/Chinese text
            mode: Translation style (natural, literal, casual, polite)
        """
        system_prompts = {
            "natural": "You are a professional manga translator. Translate the following text naturally to English, preserving the tone and emotion. Only output the translation, nothing else.",
            "literal": "Translate the following text literally to English, word-by-word. Only output the translation, nothing else.",
            "casual": "You are a fan-scan translator. Translate this manga dialogue in a casual, expressive style with slang. Only output the translation, nothing else.",
            "polite": "Translate the following text to polite, formal English. Only output the translation, nothing else."
        }
        
        system_prompt = system_prompts.get(mode, system_prompts['natural'])
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Translate: {text}"}
        ]
        
        try:
            # Format messages for ERNIE
            input_text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            # Tokenize
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.model.device)
            
            # Generate translation
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode output
            response = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            ).strip()
            
            return response
        
        except Exception as e:
            print(f"ERNIE translation error: {e}")
            return text

# Singleton instance - will be initialized on first use
_ernie_translator = None

def get_ernie_translator(model_name: str = "baidu/ERNIE-4.5-8B-Instruct") -> ERNIETranslator:
    """Get or create ERNIE translator instance"""
    global _ernie_translator
    if _ernie_translator is None:
        _ernie_translator = ERNIETranslator(model_name)
    return _ernie_translator
