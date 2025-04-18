from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.movies import schemas, services
from app.core.database import get_db

router = APIRouter(prefix="/movies", tags=["Movies"])

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
