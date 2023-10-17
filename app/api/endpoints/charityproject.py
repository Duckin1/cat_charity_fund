from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import charityproject_crud
from app.crud.donation import donation_crud
from app.schemas.charityproject import (
    CharityprojectCreate,
    CharityprojectUpdateThreeFields,
    CharityProjectResponse,
    CharityprojectBase
)
from app.schemas.donation import (
    DonationUpdate
)
from app.services import donation_handler
from app.api.validators import (
    check_name_duplicate,
    check_charityproject_exists,
    check_project_invested_amount,
    check_project_fully_invested,
    check_donation_exists,
    check_project_unic_name
)
from app.core.user import current_superuser
from typing import List
from datetime import datetime

from fastapi import HTTPException

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charityproject(
        charityproject: CharityprojectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charityproject.name, session)
    new_project = await charityproject_crud.create(charityproject, session)
    donations_not_fully_invested = await donation_handler.ProjectDonation.get_donations_not_fully_invested(session)
    if donations_not_fully_invested is not None:
        project_full_amount = new_project.full_amount
        project_full_amount_get = 'no'
        sum_to_project = 0
        for donation in donations_not_fully_invested:
            if project_full_amount_get == 'yes':
                break
            donation_amount_to_get = donation.full_amount - donation.invested_amount
            for _ in range(1, donation_amount_to_get + 1):
                sum_to_project += 1
                if project_full_amount == sum_to_project:
                    project_full_amount_get = 'yes'
                    break
            donation = await check_donation_exists(donation.id, session)
            close_date = datetime.now().isoformat(timespec='seconds')
            obj_in = DonationUpdate(
                invested_amount=sum_to_project,
                fully_invested=1,
                close_date=close_date
            )
            await donation_crud.update(donation, obj_in, session, commit_yes='no')
            if project_full_amount_get == 'yes':
                obj_in = CharityprojectUpdateThreeFields(
                    invested_amount=sum_to_project,
                    fully_invested=1,
                    close_date=close_date
                )
                await charityproject_crud.update(new_project, obj_in, session, commit_yes='no')
        await session.commit()
        await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectResponse],
    response_model_exclude_none=True,
)
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session),
):
    all_charityprojects = await charityproject_crud.get_multi(session)
    return all_charityprojects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectResponse,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
        project_id: int,
        obj_in: CharityprojectBase,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    charityproject = await check_charityproject_exists(
        project_id, session
    )

    if obj_in.name is None and obj_in.description is None and obj_in.full_amount is None:
        raise HTTPException(
            status_code=422,
            detail='Не переданы значения полей!'
        )
    await check_project_unic_name(project_id, session, obj_in.name)
    await check_project_fully_invested(project_id, session, 'редактировать')

    if obj_in.full_amount is not None:
        await check_project_invested_amount(project_id, session, 2, obj_in.full_amount)

    charityproject = await charityproject_crud.update(
        charityproject, obj_in, session
    )
    return charityproject


@router.delete(
    '/{project_id}',
    response_model=CharityProjectResponse,
    dependencies=[Depends(current_superuser)],
)
async def remove_charityproject(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):

    """Только для суперюзеров."""
    charityproject = await check_project_invested_amount(project_id, session)
    charityproject = await check_project_fully_invested(project_id, session, 'удалять')
    charityproject = await check_charityproject_exists(project_id, session)
    charityproject = await charityproject_crud.remove(charityproject, session)
    return charityproject
