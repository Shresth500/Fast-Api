import logging
import uvicorn

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from database import create_db_and_tables
from dotenv import load_dotenv
from api.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"URL: {request.url}")
    logger.info(f"HEADERS: {dict(request.headers)}")  # ✅ shows Authorization header
    response = await call_next(request)
    logger.info(f"STATUS: {response.status_code}")
    return response

app.include_router(auth_router)

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, port=8000, host="0.0.0.0")