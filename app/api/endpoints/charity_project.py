from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import CharityProjectValidator
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.charity_services import close, donate

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создать новый проект. Только для суперпользователей"""
    await CharityProjectValidator.check_name_duplicate(
        charity_project.name, session
    )
    new_project = await charity_project_crud.create(
        charity_project, session
    )
    await donate(new_project, session)
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получить список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Изменить проект. Только для суперпользователей."""
    project = await CharityProjectValidator.get_if_exists(
        project_id, session
    )
    await CharityProjectValidator.check_project_is_closed(project)

    if obj_in.name:
        await CharityProjectValidator.check_name_duplicate(
            obj_in.name, session
        )

    if obj_in.full_amount:
        project_is_full = await CharityProjectValidator.is_full_amount(
            amount=obj_in.full_amount,
            project_id=project_id,
            session=session
        )
        if project_is_full:
            await close(project)

    return await charity_project_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление проекта. Только для суперпользователей."""
    project = await CharityProjectValidator.get_if_exists(project_id, session)
    await CharityProjectValidator.check_project_is_donated(project)

    return await charity_project_crud.delete(project, session)
