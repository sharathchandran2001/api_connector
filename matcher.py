from rapidfuzz import process, fuzz
import json
from typing import Optional, Dict, Any

# Load rule-to-endpoint mappings once at module load
with open("mapping.json", "r") as f:
    rule_based_mapping = json.load(f)

def match_api_endpoint(step: str, threshold: float = 70) -> Optional[Dict[str, Any]]:
    best_match = process.extractOne(step, list(rule_based_mapping.keys()), scorer=fuzz.ratio)
    if best_match:
        keyword, score, _ = best_match
        return {
            "keyword": keyword,
            "api_endpoint": rule_based_mapping.get(keyword),
            "score": score
        }
    return None

async def match_api_endpoint_async(step: str, threshold: float = 70) -> Optional[Dict[str, Any]]:
    # Wrapped async for future concurrency expansion
    return match_api_endpoint(step, threshold)
