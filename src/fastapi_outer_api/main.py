from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

class UserRequest(BaseModel):
    username: str
    password: str
    security_question: str

# Replace with the actual endpoint of your Spring Boot API
SPRING_API_URL = "http://spring-boot-api:8080/api/process"

@app.post("/submit")
async def forward_to_spring(user: UserRequest):
    try:
        async with httpx.AsyncClient() as client:
            print(f"Forwarding request to {SPRING_API_URL} with data: {user.json()}")
            response = await client.post(
                SPRING_API_URL,
                json=user.dict(),
                timeout=10.0
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Spring API connection error: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Spring API error: {response.text}")

    return response.json()
