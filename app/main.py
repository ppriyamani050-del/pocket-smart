from pathlib import Path

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from config import settings

from app.database import init_db

from app.routes.api import router as api_router

from app.routes.pages import router as pages_router


app = FastAPI(

    title="Pocket Smart AI"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=
        settings.CORS_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

@app.get("/")
def home():
    return{"message":"API is running!"}
Path("uploads").mkdir(
    exist_ok=True
)

Path("data").mkdir(
    exist_ok=True
)


app.mount(

    "/static",

    StaticFiles(
        directory="app/static"
    ),

    name="static"
)


app.include_router(
    api_router,
    prefix="/api"
)

app.include_router(
    pages_router
)


@app.on_event("startup")
def startup():

    init_db()


@app.get("/health")
def health():

    return {

        "status": "ok",

        "app":
            settings.APP_NAME,

        "gemini_configured":
            bool(
                settings.GEMINI_API_KEY
            )
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app.main:app",

        host="127.0.0.1",

        port=8000,

        reload=True
    )