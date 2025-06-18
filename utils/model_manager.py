import asyncio
from models.inference_engine import TinyLLamaModel
from threading import Lock

class ModelManager:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.lock = Lock()
        self.model = TinyLLamaModel(model_path)

    def generate(self, prompt, max_tokens):
        with self.lock:
            return self.model.generate(prompt, max_tokens)
        
    def reload_model(self):
        with self.lock:
            print("[RELOAD]reinitializing model...")
            self.model = TinyLLamaModel(self.model_path)
            print("[RELOAD]model reinitialized successfully.")