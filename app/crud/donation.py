from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_for_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> list[Donation]:
        statement = select(Donation).where(Donation.user_id == user.id)
        donations = await session.execute(statement)
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
