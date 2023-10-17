from app.crud.base import CRUDBase
from app.models import Donation, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


donation_crud = CRUDBase(Donation)


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
