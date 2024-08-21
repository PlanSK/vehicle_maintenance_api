from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
from core.config import settings
from core.models import BaseDbModel
from core.database import db_interface
from api_v1 import router as router_v1

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_interface.engine.begin() as connection:
        await connection.run_sync(BaseDbModel.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
