from fastapi import APIRouter, HTTPException
from models import GherkinStep
from matcher import match_api_endpoint, match_api_endpoint_async
import httpx

router = APIRouter()

@router.post("/resolve-and-fetch")
async def resolve_and_fetch(step: GherkinStep):
    result = await match_api_endpoint_async(step.step)
    if not result or not result.get("api_endpoint"):
        raise HTTPException(status_code=404, detail="No matching API endpoint found.")

    method = result.get("method", "GET").upper()
    body_template = result.get("body_template", {})

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            if method == "POST":
                response = await client.post(result["api_endpoint"], json=body_template)
            else:
                response = await client.get(result["api_endpoint"])

            response.raise_for_status()
            return {
                "matched_keyword": result["keyword"],
                "api_endpoint": result["api_endpoint"],
                "method": method,
                "data": response.json()
            }

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Upstream service error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

#final_body = {**body_template, **(step.arguments or {})}
