from llama_cpp import Llama
import asyncio
import logging
from pathlib import Path

MODEL_PATH = Path("models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

def load_model():
    if not MODEL_PATH.exists():
        logging.warning("[WARN] Model file not found. Skipping model load.")
        return None
    return TinyLLamaModel(str(MODEL_PATH))

class TinyLLamaModel:
    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            n_gpu_layers=0
        )

    async def generate(self, prompt: str, max_tokens: int = 128):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_generate, prompt, max_tokens)

    def _sync_generate(self, prompt: str, max_tokens: int = 128):
        try:
            messages = [{"role": "user", "content": prompt}]
            response = ""
            for output in self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, stream=True):
                delta = output["choices"][0]["delta"]
                if "content" in delta:
                    response += delta["content"]
            return response
        except Exception as e:
            logging.error(f"[MODEL ERROR] {e}")
            raise


    def scale_down(self):
        if len(self.models) > 1:
            removed = self.models.pop()
            logging.info(f"[Manager] Scaling down: removing {removed.name}")
            del removed.model  # Clean up model resources