from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.works import Work, WorkPattern
from core.schemas.works import Work as WorkSchema
from core.schemas.works import WorkBase
from core.schemas.works import WorkPattern as WorkPatternSchema
from core.schemas.works import WorkPatternBase, WorkPatternUpdate, WorkUpdate


async def create_workpattern(
    session: AsyncSession, work_pattern_data: WorkPatternBase
) -> WorkPattern:
    work_pattern = WorkPattern(**work_pattern_data.model_dump())
    session.add(work_pattern)
    await session.commit()
    await session.refresh(work_pattern)
    return work_pattern


async def get_all_workpatterns(session: AsyncSession) -> list[WorkPattern]:
    statement = select(WorkPattern).order_by(WorkPattern.id)
    result: Result = await session.execute(statement)
    workpatterns_list: list = list(result.scalars().all())
    return workpatterns_list


async def get_workpattern_by_id(
    workpattern_id: int, session: AsyncSession
) -> WorkPattern | None:
    return await session.get(WorkPattern, workpattern_id)


async def update_workpattern(
    session: AsyncSession,
    workpattern: WorkPatternSchema,
    workpattern_update: WorkPatternUpdate,
) -> WorkPatternSchema:
    for name, value in workpattern_update.model_dump(
        exclude_unset=True
    ).items():
        setattr(workpattern, name, value)
    await session.commit()
    return workpattern


async def delete_workpattern(
    session: AsyncSession, workpattern: WorkPatternSchema
) -> None:
    await session.delete(workpattern)
    await session.commit()


async def create_work(session: AsyncSession, work_data: WorkBase) -> Work:
    work = Work(**work_data.model_dump())
    session.add(work)
    await session.commit()
    await session.refresh(work)
    return work


async def get_works_by_vehicle_id(
    session: AsyncSession, vehicle_id: int
) -> list[Work]:
    statement = select(Work).where(Work.vehicle_id == vehicle_id)
    result: Result = await session.execute(statement)
    workpatterns_list: list = list(result.scalars().all())
    return workpatterns_list


async def get_work_by_id(work_id: int, session: AsyncSession) -> Work | None:
    return await session.get(Work, work_id)


async def update_work(
    session: AsyncSession, work: WorkSchema, work_update: WorkUpdate
) -> WorkSchema:
    for name, value in work_update.model_dump(exclude_unset=True).items():
        setattr(work, name, value)
    await session.commit()
    return work


async def delete_work(session: AsyncSession, work: WorkSchema) -> None:
    await session.delete(work)
    await session.commit()
