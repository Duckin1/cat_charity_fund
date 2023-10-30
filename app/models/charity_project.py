from sqlalchemy import Column, String, Text

from .foundation_base import FoundationBase

MAX_CHARITY_PROJECTS = 100


class CharityProject(FoundationBase):
    """Модель для благотворительных проектов"""
    name = Column(String(MAX_CHARITY_PROJECTS), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'Проект: {self.name}. Собрано: {self.invested_amount}.'
