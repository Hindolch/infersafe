import asyncio
import logging
from prometheus_client import Gauge
import time


IN_FLIGHT_REQUESTS = Gauge("in_flight_requests", "Total in-flight concurrent requests")
MODEL_WORKER_COUNT = Gauge("model_worker_count", "Number of model workers")

class Autoscaler:
    def __init__(self, manager, scale_interval=5, scale_up_threshold=None, scale_down_threshold=None, min_workers=None, cooldown=None):
        self.manager = manager
        self.scale_interval = scale_interval
        self.SCALE_UP_THRESHOLD = scale_up_threshold if scale_up_threshold is not None else 5    # Requests per worker threshold for scaling up
        self.SCALE_DOWN_THRESHOLD = scale_down_threshold if scale_down_threshold is not None else 1  # Requests per worker threshold for scaling down
        self.MIN_WORKERS = min_workers if min_workers is not None else 1           # Minimum number of workers to maintain
        self.cooldown = cooldown if cooldown is not None else 15             # Seconds between scaling actions
        self.last_scale_time = 0
    
    async def start_scaling(self):
        while True:
            try:
                await asyncio.sleep(self.scale_interval)
                now = time.time()
                
                # Skip if in cooldown
                if now - self.last_scale_time < self.cooldown:
                    continue
                
                # Get current metrics
                in_flight = self.manager.total_in_flight()
                num_workers = len(self.manager.models)
                
                # Update Prometheus metrics
                IN_FLIGHT_REQUESTS.set(in_flight)
                MODEL_WORKER_COUNT.set(num_workers)
                
                # Calculate load per worker (safely handle zero workers)
                if num_workers < self.MIN_WORKERS:
                    avg_load_per_worker = float('inf')  # Force scale up if below minimum
                else:
                    avg_load_per_worker = in_flight / num_workers
                
                logging.info(
                    f"[AUTOSCALER] Status: in_flight={in_flight}, "
                    f"workers={num_workers}, avg_load={avg_load_per_worker:.2f}"
                )
                
                # Scale based on per-worker load
                if avg_load_per_worker > self.SCALE_UP_THRESHOLD:
                    logging.info(
                        f"[AUTOSCALER] Scaling UP: avg_load={avg_load_per_worker:.2f} > "
                        f"threshold={self.SCALE_UP_THRESHOLD}"
                    )
                    self.manager.scale_up()
                    self.last_scale_time = now
                elif (avg_load_per_worker < self.SCALE_DOWN_THRESHOLD 
                      and num_workers > self.MIN_WORKERS):
                    logging.info(
                        f"[AUTOSCALER] Scaling DOWN: avg_load={avg_load_per_worker:.2f} < "
                        f"threshold={self.SCALE_DOWN_THRESHOLD}"
                    )
                    self.manager.scale_down()
                    self.last_scale_time = now
                    
            except Exception as e:
                logging.error(f"[AUTOSCALER] Error in scaling loop: {e}")
                await asyncio.sleep(1)  # Back off on error
