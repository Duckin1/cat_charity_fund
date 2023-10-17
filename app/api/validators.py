from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charityproject_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charityproject_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject = await charityproject_crud.get(project_id, session)
    if charityproject is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charityproject


async def check_project_invested_amount(
        project_id: int,
        session: AsyncSession,
        trigger_operation_type: int = 1,
        full_amount: int = 0,
) -> CharityProject:
    charityproject = await charityproject_crud.get_project_with_invested_amount(project_id, session, full_amount)
    if trigger_operation_type == 1:
        if charityproject is not None:
            raise HTTPException(
                status_code=400,
                detail='В проект были внесены средства, не подлежит удалению!'
            )
    elif trigger_operation_type == 2 and charityproject is not None:
        raise HTTPException(
            status_code=422,
            detail='Нельзя устанавливать для проекта новую сумму меньше уже внесённой!'
        )
    return charityproject


async def check_project_fully_invested(
        project_id: int,
        session: AsyncSession,
        operation_type: str,
) -> CharityProject:
    charityproject = await charityproject_crud.check_project_fully_invested(project_id, session)
    if charityproject is not None:
        raise HTTPException(
            status_code=400,
            detail=f'Закрытый проект нельзя {operation_type}!'
        )
    return charityproject


async def check_donation_exists(
        donation_id: int,
        session: AsyncSession,
) -> Donation:
    donation = await donation_crud.get(donation_id, session)
    if donation is None:
        raise HTTPException(
            status_code=404,
            detail='Пожертвование не найдено!'
        )
    return donation


async def check_project_unic_name(
        project_id: int,
        session: AsyncSession,
        project_name: str
) -> CharityProject:
    charityproject = await charityproject_crud.check_project_unic_name(project_id, session, project_name)
    if charityproject is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )
    return charityproject
