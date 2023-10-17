from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityproject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_project_with_invested_amount(
            self,
            project_id: int,
            session: AsyncSession,
            full_amount: int,
    ) -> Optional[int]:

        if full_amount == 0:
            db_project_id = await session.execute(
                select(
                    CharityProject).where(
                    CharityProject.id == project_id,
                    and_(
                        CharityProject.invested_amount != 0
                    )
                )
            )
        else:
            db_project_id = await session.execute(
                select(
                    CharityProject).where(
                    CharityProject.id == project_id,
                    and_(
                        CharityProject.invested_amount > full_amount
                    )
                )
            )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def check_project_fully_invested(
            self,
            project_id: int,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(
                CharityProject).where(
                CharityProject.id == project_id,
                and_(
                    CharityProject.fully_invested == 1
                )
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def check_project_unic_name(
            self,
            project_id: int,
            session: AsyncSession,
            project_name: str
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(
                CharityProject).where(
                CharityProject.id != project_id,
                and_(
                    CharityProject.name == project_name
                )
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id


charityproject_crud = CRUDCharityproject(CharityProject)
