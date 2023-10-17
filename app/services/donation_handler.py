from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


class ProjectDonation:

    async def get_projects_not_fully_invested(
            session: AsyncSession
    ):
        charityproject = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 0
            ).order_by(CharityProject.invested_amount.desc())
        )
        if charityproject is not None:
            return charityproject.scalars().all()
        else:
            return None

    async def get_donations_not_fully_invested(
            session: AsyncSession
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.fully_invested == 0
            ).order_by(Donation.create_date.asc())
        )
        if donations is not None:
            return donations.scalars().all()
        else:
            return None
