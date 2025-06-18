from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
import os

os.environ["TESTING"] = "1"

from api.main import app

client = TestClient(app)

@patch("api.main.get_model_worker")
def test_generate_batch_success(mock_get_model):
    mock_model = AsyncMock()
    mock_model.generate.return_value = "mock response"
    mock_get_model.return_value = mock_model

    response = client.post("/generate-batch", json={"prompt": "hello", "max_tokens": 20})
    assert response.status_code == 200
    assert "mock response" in response.text
