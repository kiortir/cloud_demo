from fastapi import FastAPI

import files.router as files


def register_routers(fastapi_app: FastAPI):
    fastapi_app.include_router(files.router)


def get_app() -> FastAPI:
    app = FastAPI()
    register_routers(app)
    return app


app = get_app()
