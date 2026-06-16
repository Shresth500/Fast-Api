import logging

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from DbConnections import create_db_and_tables
from routes.chat_window_router import router as chat_window_router
from routes.auth_routes import router as auth_router
from routes.chat_routes import router as chat_router


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


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema

#     openapi_schema = get_openapi(
#         title="My FastAPI App",
#         version="1.0.0",
#         description="API with JWT Authentication",
#         routes=app.routes,
#     )

#     # Add custom information without replacing security schemes
#     openapi_schema["info"]["x-logo"] = {
#         "url": "https://example.com/logo.png"
#     }

#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi

app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(chat_window_router)