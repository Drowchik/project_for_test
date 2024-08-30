from datetime import timedelta
from datetime import datetime
from fastapi import Depends, HTTPException, Response
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy import select
from src.app.core.database import get_db
from src.app.schemas.shemas import SUserRegister
from src.app.models import User
from src.app.core.config import settings


class UserService:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    async def get_user_by_filter(db: AsyncSession, **kwargs) -> User | None:
        result = await db.execute(select(User).filter_by(**kwargs))
        return result.scalar()

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @staticmethod
    async def create_user(db: AsyncSession, email: str, hashed_password: str, name: str) -> User:
        new_user = User(
            email=email,
            name=name,
            hashed_password=hashed_password,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @classmethod
    def verify_password(cls, password: str, hash_password: str) -> bool:
        return cls.pwd_context.verify(password, hash_password)

    @classmethod
    async def register_user(cls, user_data: SUserRegister, db: AsyncSession):
        existing_user = await cls.get_user_by_filter(db, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=400, detail="Email already registered")
        hashed_password = cls.get_password_hash(user_data.password)
        await cls.create_user(db=db,
                              email=user_data.email,
                              hashed_password=hashed_password,
                              name=user_data.name)

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=45)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @classmethod
    async def login_user(cls, response: Response, user_data: SUserRegister, db: AsyncSession):
        existing_user = await cls.get_user_by_filter(db, email=user_data.email)
        if not existing_user and not cls.verify_password(user_data.password, existing_user.hashed_password):
            raise HTTPException(status_code=400, detail="Email not registered")
        access_token = cls.create_access_token({"sub": str(existing_user.id)})
        response.set_cookie("access_token_blog", access_token, httponly=True)
