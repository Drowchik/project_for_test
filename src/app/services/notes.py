from datetime import datetime
from fastapi import HTTPException
from src.app.schemas.shemas import SNotes
from src.app.models import User
from src.app.services.auth import UserService
from src.app.core.database import get_db
from fastapi_pagination import LimitOffsetPage, Params
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from src.app.models import Note, User
from sqlalchemy.orm import selectinload


class NotesService:

    @staticmethod
    async def get_my_note(user: User,
                          db: AsyncSession,
                          params: Params):
        try:
            paginated_result = await paginate(db, select(Note).filter(Note.user_id == user.id).options(selectinload(Note.category)), params)
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Erorr:  {e}")
        response = []
        for post in paginated_result.items:
            response.append(SNotes(
                title=post.title,
                description=post.description,
                username=post.user.name,
                category_name=post.category.name
            ))
        return LimitOffsetPage.create(items=response, total=paginated_result.total, params=params)

    @staticmethod
    async def add_note(note: SNotes,  user: User, db: AsyncSession):
        try:
            new_post = Note(title=note.title,
                            description=note.description, user_id=user.id)
            db.add(new_post)
            await db.commit()
            await db.refresh(new_post)
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Что-то пошло не так, пост не добавлен, ошибка {e}")
