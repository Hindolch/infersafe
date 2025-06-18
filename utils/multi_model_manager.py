import asyncio
import random
import logging
from typing import List
from models.inference_engine import TinyLLamaModel

class ModelWorker:
    def __init__(self,name:str, model_path: str):
        self.name = name
        self.model = TinyLLamaModel(model_path)
        self.lock = asyncio.Lock() #simulate load balancing by locking access
        self.in_flight_requests = 0 #track active concurrent requests
        self.semaphore = asyncio.Semaphore(4) # allow 2 concurrent prompts per worker

    async def generate(self, prompt: str, max_tokens: int):
        logging.info(f"[{self.name}] Attempting to acquire lock (in-flight: {self.in_flight_requests})")
        async with self.semaphore:
            self.in_flight_requests += 1
            try:
                logging.info(f"[{self.name}] Processing prompt: {prompt[:30]}...")
                result = await self.model.generate(prompt, max_tokens)
                logging.info(f"[{self.name}] Completed prompt: {prompt[:30]}")
                return result
            finally:
                self.in_flight_requests -= 1

class MultiModelManager:
    def __init__(self, num_workers: int, *, model_path: str):
        self.num_workers = num_workers
        self.model_path = model_path
        self.models: List[ModelWorker] = [
            ModelWorker(name=f"worker_{i}", model_path=model_path) for i in range(num_workers)
        ]

    def get_least_busy_model(self)->ModelWorker:
        #pick the least loaded model worker
        chosen =  min(self.models, key=lambda worker: worker.in_flight_requests)
        logging.info(f"[Manager] Selected {chosen.name} (in-flight: {chosen.in_flight_requests})")
        return chosen
    
    def scale_up(self):
        idx = len(self.models)
        logging.info(f"[Manager] Scaling up: spawning worker_{idx}")
        self.models.append(ModelWorker(name=f"worker_{idx}", model_path=self.model_path))
    
    def scale_down(self):
        if len(self.models) > 1:
            removed = self.models.pop()
            del removed.model  # Free resources

    def total_in_flight(self)->int:
        return sum(w.in_flight_requests for w in self.models)
    
    def reload_model(self):
        logging.info("[Manager] Reloading all model workers...")
        for worker in self.models:
            worker.model = TinyLLamaModel(self.model_path)
            logging.info(f"[Manager] Reloaded model for {worker.name}")
        logging.info("[Manager] All workers reloaded successfully.")
        return True
