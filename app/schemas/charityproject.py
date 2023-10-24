from typing import Optional
from pydantic import BaseModel, Field, PositiveInt, validator, Extra
from datetime import datetime


class CharityprojectBase(BaseModel, extra=Extra.forbid):
    """
    Основная модель для данных благотворительных проектов.

    Attributes:
        name (str, optional): Название проекта (1-100 символов).
        description (str, optional): Описание проекта (минимум 1 символ).
        full_amount (PositiveInt, optional): Полная сумма, которую необходимо собрать.

    Methods:
        full_amount_not_null(cls, value): Валидатор для проверки полноты суммы пожертвования.
        name_not_null(cls, value): Валидатор для проверки полноты названия проекта.
        description_not_null(cls, value): Валидатор для проверки полноты описания проекта.
    """

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None)

    @validator('full_amount', pre=True)
    def full_amount_not_null(cls, value):
        """
        Проверяет и валидирует полноту суммы пожертвования.

        Args:
            value: Значение суммы пожертвования.

        Returns:
            int: Проверенное и валидное значение суммы пожертвования.

        Raises:
            ValueError: Если сумма пожертвования пуста, отрицательна, равна 0 или не является целым числом.
        """
        if value == '':
            raise ValueError('Сумма пожертвования не может быть пустой!')
        elif value < 0:
            raise ValueError('Сумма пожертвования не может быть меньше 0!')
        elif value == 0:
            raise ValueError('Сумма пожертвования не может быть равна 0!')
        elif isinstance(value, int) is False:
            raise ValueError('Сумма пожертвования должна быть целым числом!')
        return value

    @validator('name', pre=True)
    def name_not_null(cls, value):
        """
        Проверяет и валидирует полноту названия проекта.

        Args:
            value: Значение названия проекта.

        Returns:
            str: Проверенное и валидное значение названия проекта.

        Raises:
            ValueError: Если название проекта пусто.
        """
        if value == '':
            raise ValueError('Название не может быть пустым!')
        return value

    @validator('description', pre=True)
    def description_not_null(cls, value):
        """
        Проверяет и валидирует полноту описания проекта.

        Args:
            value: Значение описания проекта.

        Returns:
            str: Проверенное и валидное значение описания проекта.

        Raises:
            ValueError: Если описание проекта пусто.
        """
        if value == '':
            raise ValueError('Описание не может быть пустым!')
        return value


class CharityProjectResponse(CharityprojectBase):
    """
    Модель для ответа о благотворительных проектах.

    Attributes:
        id (int): Идентификатор проекта.
        name (str, optional): Название проекта (1-100 символов).
        description (str, optional): Описание проекта (минимум 1 символ).
        full_amount (int, optional): Полная сумма, которую необходимо собрать.
        invested_amount (int): Сумма, которая уже собрана.
        fully_invested (bool): Флаг, показывающий, полностью ли проект собран.
        create_date (datetime): Дата создания проекта.
        close_date (datetime, optional): Дата закрытия проекта.

    Configuration:
        orm_mode (bool): Включает режим совместимости с ORM.
        min_anystr_length (int): Минимальная длина строковых полей.

    """

    id: int
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int] = Field(None)
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = Field(None)

    class Config:
        orm_mode = True
        min_anystr_length = 1


class CharityprojectUpdateThreeFields(BaseModel):
    """
    Модель для обновления трех полей благотворительных проектов.

    Attributes:
        invested_amount (int): Сумма, которая уже собрана.
        fully_invested (bool): Флаг, показывающий, полностью ли проект собран.
        close_date (datetime): Дата закрытия проекта (по умолчанию, текущая дата).

    """

    invested_amount: int = Field(1)
    fully_invested: bool = Field(1)
    close_date: datetime = Field(datetime.now().isoformat(timespec='seconds'))


class CharityprojectCreate(CharityprojectBase):
    """
    Модель для создания новых благотворительных проектов.

    Attributes:
        name (str): Название проекта (1-100 символов).
        description (str): Описание проекта (минимум 1 символ).
        full_amount (PositiveInt, optional): Полная сумма, которую необходимо собрать.

    """

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: Optional[PositiveInt] = Field(...)
