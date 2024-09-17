import json
from pathlib import Path

from loguru import logger
from sqlalchemy import delete, insert
from sqlalchemy.exc import IntegrityError

from .config import BASE_DIR
from .database import db_interface
from .models.works import WorkPattern


async def get_workpattern_data_from_json(json_file_path: str | Path) -> list:
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    return json_data


async def get_workpatterns_dicts_list(json_data: list) -> list[dict]:
    workpatterns_list: list = []
    for id, item in enumerate(json_data, start=1):
        item.update(id=id)
        workpatterns_list.append(item)
    return workpatterns_list


async def add_workpatterns_models_to_db() -> None:
    json_data = await get_workpattern_data_from_json(
        BASE_DIR / "works_patterns.json"
    )
    wp_data = await get_workpatterns_dicts_list(json_data)
    async with db_interface.session_factory() as session:
        try:
            await session.execute(delete(WorkPattern))
            await session.execute(insert(WorkPattern), wp_data)
            await session.commit()
        except IntegrityError as e:
            logger.error(f"Table is not empty. {e}")
