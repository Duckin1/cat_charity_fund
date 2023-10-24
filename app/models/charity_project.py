from sqlalchemy import Column, String, Text

from .foundation_base import FoundationBase


class CharityProject(FoundationBase):
    """Модель для благотворительных проектов"""
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'Проект: {self.name}. Собрано: {self.invested_amount}.'
