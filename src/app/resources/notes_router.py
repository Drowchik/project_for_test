from src.app.schemas.shemas import SNote, SNotes
from src.app.services.notes import NotesService
from src.app.models import User
from src.app.services.auth import UserService
from src.app.core.database import get_db
from fastapi_pagination import LimitOffsetPage, Params
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/notes", tags=["Заметки"],)


@router.get("/my", response_model=LimitOffsetPage)
async def get_my_note(user: User = Depends(UserService.get_current_user),
                      db: AsyncSession = Depends(get_db),
                      params: Params = Depends()):
    return NotesService.get_my_note(user, db, params)


@router.post("")
async def add_note(note: SNote,  user: User = Depends(UserService.get_current_user), db: AsyncSession = Depends(get_db)):
    await NotesService.add_note(note, user, db)
    return {"Message": "User created note successfuly"}
