import os
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.testclient import TestClient
from api.main import app, model_worker

# Set testing flag correctly
os.environ["TESTING"] = "1"

# Patch the actual model inference to avoid heavy lifting
model_worker.generate = AsyncMock(return_value="mock response")

client = TestClient(app)

def test_generate_batch_success():
    response = client.post("/generate-batch", json={"prompt": "hello", "max_tokens": 20})
    assert response.status_code == 200
    text = response.text.strip()
    assert "Error" not in text, f"Failed with error: {text}"
    assert len(text.split()) > 0
