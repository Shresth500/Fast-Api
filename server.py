from fastapi import FastAPI
from DbConnections import create_db_and_tables
from routes.chat_routes import router as chat_router
from routes.auth_routes import router as auth_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI): 
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    
    return {
        "status": "Server is up and running"
    }

app.include_router(chat_router)
app.include_router(auth_router)