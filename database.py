from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from schema import UserAdd, UserId, User


engine = create_async_engine("sqlite+aiosqlite:///db//fastapi.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class UserOrm(Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str]
    age: Mapped[int]
    phone :Mapped[str|None]


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

class UserRepository:

    @classmethod
    async def add_user(cls, user:UserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump()
            user = UserOrm(**data)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
        

    @classmethod
    async def update_user(cls, user:User) -> str:
        async with new_session() as session:
            query = select(UserOrm).filter(UserOrm.id == user.id)
            res = await session.execute(query)
            user2 = res.scalars().first()
            str2 = 'OK'
            if user2 is None:
                str2 = 'Нет такого пользователя'
            else:
                user2.age = user.age
                user2.name = user.name
                user2.phone = user.phone
            await session.flush()
            await session.commit()
            return str2
        
    @classmethod
    async def remove_user(cls, user:UserId) -> str:
        async with new_session() as session:
            query = select(UserOrm).filter(UserOrm.id == user.id)
            res = await session.execute(query)
            user = res.scalars().first()
            str2 = 'OK'
            if user is None:
                str2 = 'Нет такого пользователя'
            else:
                try:
                    await session.delete(user)
                except Exception:
                    str2 = 'Произошла ошибка при удалении'
            await session.flush()
            await session.commit()
            return str2 
        
    @classmethod
    async def get_users(cls) -> list[UserOrm]:
        async with new_session() as session:
            query = select(UserOrm)
            res = await session.execute(query)
            users = res.scalars().all()
            return users