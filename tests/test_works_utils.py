import random
from sqlalchemy import select
from api_v1.works.utils import create_works_on_create_vehicle
from core.database import db_handler
from core.models.vehicle import Vehicle
from core.models.workpattern import WorkPattern
from core.models.works import Work


async def test_create_works_on_create_vehicle(
    vehicle_test_models_list: list[Vehicle], vehicles_add_to_db
):
    test_vehicle_model = random.choice(vehicle_test_models_list)
    async for db_session in db_handler.get_db():
        async with db_session as session:
            await create_works_on_create_vehicle(
                vehicle_id=test_vehicle_model.id, session=session
            )
            workpatterns = await session.scalars(select(WorkPattern))
            works_result = await session.scalars(
                select(Work).where(Work.vehicle_id == test_vehicle_model.id)
            )
    workpatterns_list: list[WorkPattern] = list(workpatterns)
    works_list: list[Work] = list(works_result)
    assert len(workpatterns_list) == len(works_list)
    for workpattern, work in zip(workpatterns_list, works_list):
        assert workpattern.title == work.title
