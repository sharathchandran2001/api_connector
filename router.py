from fastapi import APIRouter, HTTPException
from models import GherkinStep
from matcher import match_api_endpoint, match_api_endpoint_async
import httpx

router = APIRouter()

@router.post("/translate")
def translate_gherkin(step: GherkinStep):
    result = match_api_endpoint(step.step)
    if result:
        if result["score"] < 70:
            return {
                "message": "No high-confidence match found; returning closest match as fallback.",
                "fallback": result
            }
        return result
    raise HTTPException(status_code=404, detail="No match found and fallback mapping is empty.")

@router.post("/translate/async")
async def translate_gherkin_async(step: GherkinStep):
    result = await match_api_endpoint_async(step.step)
    if result:
        if result["score"] < 70:
            return {
                "message": "No high-confidence match found; returning closest match as fallback.",
                "fallback": result
            }
        return result
    raise HTTPException(status_code=404, detail="No match found and fallback mapping is empty.")

@router.post("/resolve-and-fetch")
async def resolve_and_fetch(step: GherkinStep):
    result = await match_api_endpoint_async(step.step)
    if not result or not result.get("api_endpoint"):
        raise HTTPException(status_code=404, detail="No matching API endpoint found.")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(result["api_endpoint"])
            response.raise_for_status()
            return {
                "matched_keyword": result["keyword"],
                "api_endpoint": result["api_endpoint"],
                "score": result["score"],
                "data": response.json()
            }
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Upstream service error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
