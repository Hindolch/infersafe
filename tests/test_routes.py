from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
import os
import pytest

# Skip all tests in CI if model path is missing
if os.getenv("CI") == "true":
    pytest.skip("Skipping tests in CI: model path not found", allow_module_level=True)

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_prompt_endpoint_schema():
    response = client.post("/prompt/", json={"prompt": "Write a story about AI"})
    assert response.status_code == 200
    assert "response" in response.json()

@patch("api.main.get_model_worker")
def test_generate_batch_success(mock_get_model):
    mock_model = AsyncMock()
    mock_model.generate.return_value = "mock response"
    mock_get_model.return_value = mock_model

    response = client.post("/generate-batch", json={"prompt": "hello", "max_tokens": 20})
    assert response.status_code == 200
    assert "mock response" in response.text
