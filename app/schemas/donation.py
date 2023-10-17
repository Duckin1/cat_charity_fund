from datetime import datetime
from pydantic import BaseModel, Extra, Field, PositiveInt
from typing import Optional


class DonationBase(BaseModel):
    id: int
    comment: str = Field(None)
    full_amount: int = Field(1)
    create_date: datetime

    class Config:
        extra = Extra.forbid


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreateResponse(BaseModel):
    full_amount: int = Field(1)
    comment: Optional[str]
    id: int
    create_date: datetime = Field(...)

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    user_id: Optional[int]
    fully_invested: bool
    invested_amount: int

    class Config:
        orm_mode = True


class DonationUpdate(BaseModel):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = Field(None)


class DonationMy(BaseModel):
    comment: str = Field(...)
    create_date: datetime
    full_amount: int = Field(1)
    id: int

    class Config:
        orm_mode = True