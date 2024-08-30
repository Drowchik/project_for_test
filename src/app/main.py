from fastapi import FastAPI
from src.app.resources.notes import router as router_notes


def get_app():
    app = FastAPI(title="Kode Education",
                  description="A test assignment from Denis Sergeev")
    app.include_router(router=router_notes)
    return app
