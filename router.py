from fastapi import APIRouter
from schema import *
from fastapi import FastAPI, Depends
from database import UserRepository



user_router = APIRouter(
    prefix="/users",
    tags=['users']
)


@user_router.post('')
async def add_user(user: UserAdd = Depends()) -> UserId:
    id = await UserRepository.add_user(user)
    return {"id":id}


@user_router.get('')
async def get_users() -> list[User]:
    users = await UserRepository.get_users()
    return users

@user_router.delete('')
async def remove_user(user: UserId = Depends()) -> Errorcode:
    res = await UserRepository.remove_user(user)
    return {"res":res}

@user_router.put('')
async def update_user(user: User = Depends()) -> Errorcode:
    res = await UserRepository.update_user(user)
    return {"res":res}