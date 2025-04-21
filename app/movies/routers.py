from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.movies import schemas, services
from app.core.database import get_db
from app.user.dependencies import get_current_user

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get(
    "/",
    response_model=List[schemas.MovieRead],
    summary="Filter movies",
    description="Returns a list of movies filtered by name, IMDB rating, price, and release year."
)
def filter_movies(
    name: Optional[str] = None,
    min_imdb: Optional[float] = None,
    max_imdb: Optional[float] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Get a list of movies filtered by optional parameters:
    - `name`: partial or full movie title
    - `min_imdb` / `max_imdb`: IMDB rating range
    - `min_price` / `max_price`: price range
    - `year`: release year
    """
    return services.filter_movies(db, name, min_imdb, max_imdb, min_price, max_price, year)


@router.post(
    "/",
    response_model=schemas.MovieRead,
    summary="Create a new movie",
    description="Adds a new movie to the database. Only accessible to authorized users (e.g. admins)."
)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    """
    Create a new movie in the database.
    """
    return services.create_movie(db, movie)


@router.get(
    "/",
    response_model=List[schemas.MovieRead],
    summary="List movies",
    description="Returns a paginated list of all available movies."
)
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of movies with pagination.
    """
    return services.get_movies(db, skip, limit)


@router.get(
    "/{movie_id}",
    response_model=schemas.MovieRead,
    summary="Get movie by ID",
    description="Returns detailed information about a specific movie by its ID."
)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Get movie details by ID. Raises 404 if not found.
    """
    movie = services.get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.post(
    "/reactions/",
    summary="Add a reaction to a movie",
    description="Allows an authenticated user to like or dislike a specific movie."
)
def create_reaction(
    reaction: schemas.MovieReactionCreate,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_user)
):
    """
    Create a like/dislike reaction for a movie.
    """
    return services.create_movie_reaction(db=db, reaction=reaction)


@router.get(
    "/reactions/{movie_id}",
    summary="Get reactions for a movie",
    description="Returns the number of likes and dislikes for a given movie."
)
def get_reactions(movie_id: int, db: Session = Depends(get_db)):
    """
    Get total reactions (likes/dislikes) for a movie.
    """
    reactions = services.get_movie_reactions(db=db, movie_id=movie_id)
    if not reactions:
        raise HTTPException(status_code=404, detail="No reactions found for this movie")
    return reactions


@router.post(
    "/comments/",
    response_model=schemas.CommentRead,
    summary="Add a comment to a movie",
    description="Allows an authenticated user to leave a comment on a movie."
)
def add_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_user)
):
    """
    Leave a comment on a movie.
    """
    return services.create_comment(db, comment)

