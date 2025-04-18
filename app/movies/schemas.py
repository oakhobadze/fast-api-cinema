from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional, List


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
    comments: List["CommentRead"] = []

    model_config = ConfigDict(from_attributes=True)

class CommentCreate(BaseModel):
    movie_id: int
    text: str


class CommentRead(BaseModel):
    id: int
    text: str

    model_config = ConfigDict(from_attributes=True)

class ReactionEnum(str, Enum):
    like = "like"
    dislike = "dislike"


class MovieReactionBase(BaseModel):
    movie_id: int
    reaction_type: str

    model_config = ConfigDict(from_attributes=True)


class MovieReactionCreate(BaseModel):
    movie_id: int
    reaction: ReactionEnum

    model_config = ConfigDict(from_attributes=True)


class MovieReaction(MovieReactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
