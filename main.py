from fastapi import FastAPI
from router import router

app = FastAPI(title="Gherkin to API Middleware")

# Include routes from router
app.include_router(router)
