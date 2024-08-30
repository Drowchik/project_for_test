

from fastapi import APIRouter


router = APIRouter(prefix="/notes", tags=["Заметки"],)


@router.get("")
async def hello():
    return {"message": "hello"}
