from fastapi import FastAPI
from pydantic import BaseModel
from nlp_fuzzy import extract_rule
from router import get_endpoints
from aggregator import fetch_all
from utils import log_info

app = FastAPI()

class Payload(BaseModel):
    query: str

@app.post("/match-data")
async def match_data(payload: Payload):
    log_info(f"Received request with query: {payload.query}")
    rule = extract_rule(payload.query)
    endpoints = get_endpoints(rule)

    if not endpoints:
        return {"error": "No endpoint found for matched rule."}

    data = await fetch_all(endpoints)
    return {
        "matched_rule": rule,
        "queried_endpoints": endpoints,
        "results": data
    }
