from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models import User
from src.app.core.database import get_db
from src.app.schemas.shemas import SUser, SUserRegister
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


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token_blog")
    return {"message": "Logged out successfully."}


@router.get("/me")
async def read_users_me(current_user: User = Depends(UserService.get_current_user)):
    return SUser(name=current_user.name, email=current_user.email)
