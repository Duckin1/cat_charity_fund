from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationDBBase
)
from app.services.charity_services import donate


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBBase,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Создать пожертвование от текущего пользователя."""
    new_donation = await donation_crud.create(donation, session, user)
    await donate(new_donation, session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Получить список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDBBase],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def get_current_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получить все пожертвования текущего пользователя."""
    return await donation_crud.get_for_user(user, session)
