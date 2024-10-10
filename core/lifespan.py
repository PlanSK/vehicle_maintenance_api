from loguru import logger
from sqlalchemy import delete, insert
from sqlalchemy.exc import IntegrityError

from core.config import BASE_DIR
from core.database import db_interface
from core.models.workpattern import WorkPattern
from core.utils import (
    get_workpattern_data_from_json,
    get_workpatterns_dicts_list,
)


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
