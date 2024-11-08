from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.workpattern import WorkPattern
from core.schemas.workpattern import (
    WorkPatternBase,
    WorkPatternSchema,
    WorkPatternUpdate,
)


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
