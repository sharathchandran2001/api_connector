from external_connector import fetch_data
import asyncio

async def fetch_all(endpoints: list) -> dict:
    tasks = [fetch_data(ep) for ep in endpoints]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    response_map = {}
    for idx, res in enumerate(results):
        key = endpoints[idx]
        if isinstance(res, Exception):
            response_map[key] = {"error": str(res)}
        else:
            response_map[key] = res
    return response_map
