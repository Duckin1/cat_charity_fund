from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        statement = select(
            CharityProject.id
        ).where(
            CharityProject.name == project_name
        )
        db_project_id = await session.execute(statement)
        return db_project_id.scalars().first()

    async def update(
            self,
            db_project: CharityProject,
            project_in: CharityProjectUpdate,
            session: AsyncSession
    ) -> CharityProject:
        project_data = jsonable_encoder(db_project)
        update_data = project_in.dict(exclude_unset=True)
        for field in project_data:
            if field in update_data:
                setattr(db_project, field, update_data[field])
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project

    async def delete(
            self,
            db_project: CharityProject,
            session: AsyncSession,
    ) -> CharityProject:
        await session.delete(db_project)
        await session.commit()
        return db_project


charity_project_crud = CRUDCharityProject(CharityProject)
