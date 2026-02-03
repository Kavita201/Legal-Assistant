import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

class SimpleLLM:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    @st.cache_resource
    def _load_model(_self):
        try:
            model_name = "distilgpt2"  # Lightweight model
            _self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            _self.model = AutoModelForCausalLM.from_pretrained(model_name)
            _self.tokenizer.pad_token = _self.tokenizer.eos_token
            return True
        except:
            return False
    
    def generate_text(self, prompt: str, max_length: int = 100) -> str:
        if not self.model:
            return "LLM not available"
        
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncate=True, max_length=50)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs, 
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return generated[len(prompt):].strip()
        except:
            return "Generation failed"

# Legal-specific prompts
LEGAL_PROMPTS = {
    "summary": "This contract is about",
    "risk_assessment": "The main legal risks are",
    "suggestions": "Legal recommendations:",
    "compliance": "For Indian law compliance"
}