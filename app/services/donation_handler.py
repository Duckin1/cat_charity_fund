from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


class ProjectDonation:

    async def get_projects_not_fully_invested(session: AsyncSession):
        """
        Получить список благотворительных проектов, которые не полностью финансированы.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            list[CharityProject] или None: Список экземпляров CharityProject, которые не полностью финансированы,
            или None, если такие проекты не найдены.

        Примечание:
        Функция выполняет запрос к базе данных для поиска экземпляров CharityProject, у которых атрибут 'fully_invested'
        установлен в 0 (показывая, что они не полностью финансированы). Результаты упорядочиваются по 'invested_amount' в
        порядке убывания.

        """

        charityproject = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 0
            ).order_by(CharityProject.invested_amount.desc())
        )
        if charityproject is not None:
            return charityproject.scalars().all()
        else:
            return None

    async def get_donations_not_fully_invested(session: AsyncSession):
        """
        Получить список пожертвований, которые не полностью финансированы.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            list[Donation] или None: Список экземпляров Donation, которые не полностью финансированы,
            или None, если такие пожертвования не найдены.

        Примечание:
        Функция выполняет запрос к базе данных для поиска экземпляров Donation, у которых атрибут 'fully_invested'
        установлен в 0 (показывая, что они не полностью финансированы). Результаты упорядочиваются по 'create_date' в
        порядке возрастания.

        """

        donations = await session.execute(
            select(Donation).where(
                Donation.fully_invested == 0
            ).order_by(Donation.create_date.asc())
        )
        if donations is not None:
            return donations.scalars().all()
        else:
            return None
