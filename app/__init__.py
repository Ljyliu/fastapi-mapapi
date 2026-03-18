from fastapi import FastAPI
from app.api.v1.api import api_v1

def create_app() -> FastAPI:
    app = FastAPI()

    
    app.include_router(api_v1, prefix="/api/v1")

    return app