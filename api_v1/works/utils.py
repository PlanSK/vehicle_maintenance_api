from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.workpatterns.crud import get_all_workpatterns
from core.models.works import Work
from core.schemas.workpattern import WorkPatternSchema


async def create_works_on_create_vehicle(
    vehicle_id: int, session: AsyncSession
) -> None:
    workpatterns_list = await get_all_workpatterns(session=session)
    wp_dicts_list = []
    for workpattern in workpatterns_list:
        wp_dict = WorkPatternSchema.model_validate(workpattern).model_dump()
        wp_dict.update(vehicle_id=vehicle_id, note="")
        wp_dicts_list.append(wp_dict)
    await session.execute(insert(Work), wp_dicts_list)
    await session.commit()
