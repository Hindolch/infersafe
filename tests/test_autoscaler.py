import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import pytest
from utils.autoscaler import Autoscaler  # Adjust import path as needed

class DummyManager:
    def __init__(self):
        self.models = [1, 2]
        self.calls = []

    def total_in_flight(self):
        return 6

    def scale_up(self):
        self.calls.append("up")

    def scale_down(self):
        self.calls.append("down")

@pytest.mark.asyncio
async def test_autoscaler_scale_up():
    manager = DummyManager()
    scaler = Autoscaler(manager, scale_interval=0.05, scale_up_threshold=2, cooldown=0)  # cooldown 0 for fast test

    scaling_task = asyncio.create_task(scaler.start_scaling())

    await asyncio.sleep(0.2)  # Let it run briefly

    assert "up" in manager.calls

    # Cancel the infinite loop
    scaling_task.cancel()
    try:
        await scaling_task
    except asyncio.CancelledError:
        pass
