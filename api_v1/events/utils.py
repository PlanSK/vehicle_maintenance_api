from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.vehicles.utils import update_vehicle_mileage_from_event
from api_v1.works.crud import get_work_by_id
from core.models import Event


async def get_average_mileage_interval(events_list: list[Event]) -> int:
    mileages_list = [event.mileage for event in events_list]
    event_counter = len(mileages_list)
    if event_counter <= 1:
        return 0
    previous_mileage = mileages_list[0]
    mileage_delta_sum = 0
    for mileage in mileages_list:
        mileage_delta_sum += mileage - previous_mileage
        previous_mileage = mileage
    return mileage_delta_sum // (event_counter - 1)


async def update_vehicle_mileage_from_work_event(
    work_id: int, event_mileage: int, session: AsyncSession
) -> None:
    if work := await get_work_by_id(work_id=work_id, session=session):
        await update_vehicle_mileage_from_event(
            session=session,
            vehicle_id=work.vehicle_id,
            event_mileage=event_mileage,
        )
    else:
        logger.error(f"Work with id {work_id} not found in db.")
