import asyncio
from typing import List, Callable
import logging

BATCH_SIZE_LIMIT = 10  # Maximum number of requests per batch

class BatchedRequest:
    def __init__(self, prompt: str, max_tokens: int, future: asyncio.Future):
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.future = future
        

class RequestQueueManager:
    def __init__(self, batch_interval: int = 100, max_queue_size: int = 100):
        self.queue: List[BatchedRequest] = []
        self.batch_interval = batch_interval / 1000
        self.max_queue_size = max_queue_size

    def enqueue(self, prompt: str, max_tokens: int) -> asyncio.Future:
        if len(self.queue) >= self.max_queue_size:
            # Return error future if queue is full
            loop = asyncio.get_event_loop()
            future = loop.create_future()
            future.set_exception(Exception("Request queue is full, try again later"))
            return future

        loop = asyncio.get_event_loop()
        future = loop.create_future()
        logging.info(f"[QUEUE] Enqueuing prompt: {prompt[:30]}, queue size: {len(self.queue)}")
        self.queue.append(BatchedRequest(prompt, max_tokens, future))
        return future

    async def start_loop(self, process_batch: Callable[[List[BatchedRequest]], None]):
        while True:
            try:
                await asyncio.sleep(self.batch_interval)
                if self.queue:
                    # Process in chunks of BATCH_SIZE_LIMIT
                    remaining = len(self.queue)
                    start_idx = 0
                    while remaining > 0:
                        batch_size = min(BATCH_SIZE_LIMIT, remaining)
                        batch = self.queue[start_idx:start_idx + batch_size]
                        asyncio.create_task(process_batch(batch))
                        start_idx += batch_size
                        remaining -= batch_size
                    self.queue = self.queue[start_idx:]
            except Exception as e:
                logging.error(f"Error in batch processing loop: {e}")
                await asyncio.sleep(1)  # Back off on error
