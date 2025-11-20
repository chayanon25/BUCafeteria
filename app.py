from fastapi import FastAPI
from models import create_db_and_tables
from contextlib import asynccontextmanager
from restaurant_router import router as restaurant_router
 
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
 
 
app = FastAPI(lifespan=lifespan)
app.include_router(restaurant_router)