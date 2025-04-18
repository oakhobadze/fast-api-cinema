import uuid
from typing import Optional

from sqlalchemy.orm import Session
from app.movies import models, schemas

def create_certification(db: Session, cert: schemas.CertificationCreate):
    db_cert = models.Certification(**cert.dict())
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict(), uuid=str(uuid.uuid4()))
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def get_movie_by_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def create_movie_reaction(db: Session, reaction: schemas.MovieReactionCreate):
    db_reaction = models.MovieReaction(movie_id=reaction.movie_id, reaction=reaction.reaction)
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction

def get_movie_reactions(db: Session, movie_id: int):
    return db.query(models.MovieReaction).filter(models.MovieReaction.movie_id == movie_id).all()

def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def filter_movies(
    db: Session,
    name: Optional[str],
    min_imdb: Optional[float],
    max_imdb: Optional[float],
    min_price: Optional[float],
    max_price: Optional[float],
    year: Optional[int],
):
    query = db.query(models.Movie)

    if name:
        query = query.filter(models.Movie.name.ilike(f"%{name}%"))
    if min_imdb is not None:
        query = query.filter(models.Movie.imdb >= min_imdb)
    if max_imdb is not None:
        query = query.filter(models.Movie.imdb <= max_imdb)
    if min_price is not None:
        query = query.filter(models.Movie.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Movie.price <= max_price)
    if year:
        query = query.filter(models.Movie.year == year)

    return query.all()

