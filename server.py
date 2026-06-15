from fastapi import FastAPI
from DbConnections import create_db_and_tables
from routes.chat_routes import router as chat_router
from routes.auth_routes import router as auth_router
from contextlib import asynccontextmanager
from fastapi.middleware.trustedhost import TrustedHostMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI): 
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]  
)


@app.get("/")
def root():
    
    return {
        "status": "Server is up and running"
    }

app.include_router(chat_router)
app.include_router(auth_router)