from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID

class CertificationBase(BaseModel):
    name: str

class CertificationCreate(CertificationBase):
    pass

class CertificationRead(CertificationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieBase(BaseModel):
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: str
    price: float
    certification_id: Optional[int] = None

class MovieCreate(MovieBase):
    pass

class MovieRead(MovieBase):
    id: int
    uuid: UUID
    certification: Optional[CertificationRead] = None

    model_config = ConfigDict(from_attributes=True)
