from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.database import get_db
from src.app.schemas.shemas import SUserRegister
from src.app.services.auth import UserService


router = APIRouter(prefix="/auth",
                   tags=["Пользователи"],)


@router.post("/register")
async def register_user(user_data: SUserRegister, db: AsyncSession = Depends(get_db)):
    try:
        await UserService.register_user(user_data, db)
        return {"Message": "User registered successfuly"}
    except HTTPException as e:
        raise e


@router.post("/login")
async def login_user(response: Response, user_data: SUserRegister, db: AsyncSession = Depends(get_db)):
    await UserService.login_user(response, user_data, db)
    return {"Message": "User logged successfuly"}
