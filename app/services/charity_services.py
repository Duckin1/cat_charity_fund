from datetime import datetime
from typing import Type, TypeVar, Union

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation

ModelType = TypeVar('ModelType', CharityProject, Donation)


async def close(obj: Union[CharityProject, Donation]) -> None:
    """Закрыть проект или пожертвование."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def get_open_objects(
    model: Type[ModelType],
    session: AsyncSession,
) -> list[Union[CharityProject, Donation]]:
    """Получить все незавершенные проекты или пожертвования."""
    statement = select(
        model
    ).where(
        model.fully_invested == false()
    ).order_by(
        model.create_date
    )
    open_objs = await session.execute(statement)

    return open_objs.scalars().all()


async def donate(
    obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """Распределить пожертвования по незавершенным проектам."""
    target = Donation if isinstance(obj, CharityProject) else CharityProject

    queue_to_distribution = await get_open_objects(target, session)
    if not queue_to_distribution:
        return

    available_quantity = obj.full_amount
    for elem in queue_to_distribution:
        deficit = elem.full_amount - elem.invested_amount
        invested_amount = min(deficit, available_quantity)
        elem.invested_amount += invested_amount
        obj.invested_amount += invested_amount
        available_quantity -= invested_amount

        if elem.full_amount == elem.invested_amount:
            await close(elem)

        if not available_quantity:
            await close(obj)
            break
    await session.commit()
