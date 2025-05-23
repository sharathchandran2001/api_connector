from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import httpx

app = FastAPI()

# Spring Boot API endpoints
SPRING_API_SUBMIT_URL = "http://spring-boot-api:8080/api/process"
SPRING_API_ACCT_URL = "http://spring-boot-api:8080/api/accountdetails"

# Model for individual user in the list
class UserRequest(BaseModel):
    username: str
    password: str
    security_question: str

# Request model that wraps multiple users
class CustomerListRequest(BaseModel):
    customerList: List[UserRequest]

# Request model for /accountdetails
class AccountDetailsRequest(BaseModel):
    ssn: str
    username: str
    security_question: str

@app.post("/submit")
async def forward_to_spring(customer_list: CustomerListRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                SPRING_API_SUBMIT_URL,
                json=customer_list.dict(),
                timeout=10.0
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Spring API connection error: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Spring API error: {response.text}")

    return response.json()

@app.post("/accountdetails")
async def forward_account_details(account: AccountDetailsRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                SPRING_API_ACCT_URL,
                json=account.dict(),
                timeout=10.0
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Spring API connection error: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Spring API error: {response.text}")

    return response.json()
