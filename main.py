from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

from api_v1 import router as router_v1
from core.config import settings
from core.utils import add_workpatterns_models_to_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await add_workpatterns_models_to_db()
    yield


app = FastAPI(lifespan=lifespan, docs_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + "-Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


if app.swagger_ui_oauth2_redirect_url:

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
