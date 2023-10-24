from sqlalchemy import Column, ForeignKey, Integer, Text

from .foundation_base import FoundationBase


class Donation(FoundationBase):
    """Модель для пожертвований"""
    comment = Column(Text)
    user_id = Column(
        Integer,
        ForeignKey('user.id',)
    )
