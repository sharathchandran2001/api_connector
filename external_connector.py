import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from utils import log_info

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def fetch_data(endpoint: str) -> dict:
    log_info(f"Calling endpoint: {endpoint}")
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(endpoint)
        response.raise_for_status()
        return response.json()
