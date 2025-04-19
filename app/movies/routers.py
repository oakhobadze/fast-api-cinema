from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.movies import schemas, services
from app.core.database import get_db
from app.user.dependencies import get_current_user

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/", response_model=List[schemas.MovieRead])
def filter_movies(
    name: Optional[str] = None,
    min_imdb: Optional[float] = None,
    max_imdb: Optional[float] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return services.filter_movies(db, name, min_imdb, max_imdb, min_price, max_price, year)

@router.post("/", response_model=schemas.MovieRead)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return services.create_movie(db, movie)

@router.get("/", response_model=list[schemas.MovieRead])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return services.get_movies(db, skip, limit)

@router.get("/{movie_id}", response_model=schemas.MovieRead)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = services.get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.post("/reactions/")
def create_reaction(
    reaction: schemas.MovieReactionCreate,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_user)
):
    return services.create_movie_reaction(db=db, reaction=reaction)

@router.get("/reactions/{movie_id}")
def get_reactions(movie_id: int, db: Session = Depends(get_db)):
    reactions = services.get_movie_reactions(db=db, movie_id=movie_id)
    if not reactions:
        raise HTTPException(status_code=404, detail="No reactions found for this movie")
    return reactions


@router.post("/comments/", response_model=schemas.CommentRead)
def add_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_user)
):
    return services.create_comment(db, comment)

