import pytest
import asyncio
import httpx

MAX_RETRIES = 2

async def send_request(i):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                r = await client.post(
                    "http://localhost:8000/generate-batch",
                    json={"prompt": f"Write me a haiku about autumn {i}", "max_tokens": 20},
                )
                print(f"[{i}] Attempt {attempt}: {r.status_code} - {r.text}")
                assert r.status_code == 200
                return
        except Exception as e:
            print(f"[{i}] Attempt {attempt} failed with error: {e}")
            if attempt == MAX_RETRIES:
                pytest.fail(f"[{i}] All retries failed: {e}")

@pytest.mark.asyncio
async def test_load_batch():
    tasks = [send_request(i) for i in range(10)]
    await asyncio.gather(*tasks)
