from app.core.user import current_superuser, current_user
from app.models import User
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import donation_handler
from app.api.validators import (
    check_charityproject_exists,
)
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.crud.charityproject import charityproject_crud
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationUpdate, DonationMy, DonationCreateResponse
)

from app.schemas.charityproject import (
    CharityprojectUpdateThreeFields
)

from datetime import datetime

router = APIRouter()


@router.post('/',
             response_model=DonationCreateResponse,
             response_model_exclude_none=True
             )
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation, session, user
    )
    projects_not_fully_invested = await donation_handler.ProjectDonation.get_projects_not_fully_invested(session)
    if projects_not_fully_invested is not None:
        donation_current_amount = donation.full_amount
        donation_left = donation.full_amount
        donation_current_left_global = 0
        for project in projects_not_fully_invested:
            if donation_current_amount == 0:
                break
            project_invested_amount = project.invested_amount
            donation_current_left = 0
            while donation_current_amount > 0:
                project_invested_amount += 1
                donation_current_left += 1
                if project_invested_amount == project.full_amount:
                    donation_current_amount -= 1
                    break
                donation_current_amount -= 1
            donation_left -= donation_current_left
            donation_current_left_global += donation_current_left
            charityproject = await check_charityproject_exists(project.id, session)
            fully_invested_cur = 0
            # close_date = project.close_date
            if project.full_amount == donation_current_left + project.invested_amount:
                fully_invested_cur = 1
            close_date = datetime.now().isoformat(timespec='seconds')
            obj_in = CharityprojectUpdateThreeFields(
                invested_amount=project.invested_amount + donation_current_left,
                fully_invested=fully_invested_cur,
                close_date=close_date
            )
            await charityproject_crud.update(charityproject, obj_in, session, commit_yes='no')
        if donation_left != donation.full_amount:
            close_date = new_donation.close_date
            fully_invested = 0
            if donation_current_left_global == new_donation.full_amount:
                fully_invested = 1
                close_date = datetime.now().isoformat(timespec='seconds')
            obj_in = DonationUpdate(
                invested_amount=donation_current_left_global,
                fully_invested=fully_invested,
                close_date=close_date
            )
            await donation_crud.update(new_donation, obj_in, session, commit_yes='no')
        await session.commit()
        await session.refresh(new_donation)
    return new_donation


@router.get('/',
            response_model=list[DonationDB],
            dependencies=[Depends(current_superuser)],
            )
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):

    """Только для суперюзеров."""

    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationMy],
    response_model_exclude={'user_id'},
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех пожертвований для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
