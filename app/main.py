from fastapi import FastAPI

from .routes.api import router as api_router

app = FastAPI(title="Financial Statement API")

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Financial Statement API is running"}
