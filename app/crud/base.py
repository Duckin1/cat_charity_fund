from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_by_attribute(
            self,
            attribute_name: str,
            attribute_value: str,
            session: AsyncSession,
    ):
        attr = getattr(self.model, attribute_name)
        statement = select(self.model).where(attr == attribute_value)
        db_obj = await session.execute(statement)
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_data = obj_in.dict()
        if user:
            obj_data['user_id'] = user.id
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
