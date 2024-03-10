# pip install fastapi 
#       uvicorn pydantic aiosqlite sqlalchemy

from fastapi import FastAPI
from schema import UserAdd, User, UserId
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("------Bases build-------------")
    yield
    await delete_tables()
    print("-------------Bases droped------------")


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)