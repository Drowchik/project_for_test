from fastapi import FastAPI
from src.app.resources.notes import router as router_notes
from src.app.resources.user_router import router as user_router


def get_app():
    app = FastAPI(title="Kode Education",
                  description="A test assignment from Denis Sergeev")
    app.include_router(router=router_notes)
    app.include_router(router=user_router)
    return app
