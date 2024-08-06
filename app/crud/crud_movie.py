from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.models.movie import Movie
from app.db.models.rating import Rating
from app.db.schemas.movie import MovieCreate, MovieUpdate
from app.logger.logger import logger
from uuid import UUID

def create_movie(db: Session, movie: MovieCreate, user_id: UUID):
    logger.info("Creating a new movie.")
    db_movie = Movie(**movie.dict(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    logger.info(f"Movie created with title: {movie.title}")
    return db_movie

def get_movie(db: Session, movie_id: UUID):
    logger.info(f"Fetching movie by ID: {movie_id}")
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie:
        logger.info(f"Movie found with ID: {movie_id}")
    else:
        logger.warning(f"Movie not found with ID: {movie_id}")
    return movie

def get_movies(db: Session, skip: int = 0, limit: int = 10, search: str = None):
    logger.info("Fetching movies list.")
    query = db.query(Movie)
    if search:
        logger.info(f"Applying search filter: {search}")
        query = query.filter(or_(Movie.title.contains(search), Movie.description.contains(search)))
    movies = query.offset(skip).limit(limit).all()
    logger.info(f"Movies retrieved: {len(movies)}")
    return movies

def update_movie(db: Session, movie_id: UUID, movie: MovieUpdate):
    logger.info(f"Updating movie with ID: {movie_id}")
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie:
        for key, value in movie.dict(exclude_unset=True).items():
            setattr(db_movie, key, value)
        db.commit()
        db.refresh(db_movie)
        logger.info(f"Movie updated with ID: {movie_id}")
    else:
        logger.warning(f"Movie not found with ID: {movie_id}")
    return db_movie

def delete_movie(db: Session, movie_id: UUID):
    logger.info(f"Deleting movie with ID: {movie_id}")
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie:
        logger.info(f"Deleting related ratings for movie ID: {movie_id}")
        db.query(Rating).filter(Rating.movie_id == movie_id).delete(synchronize_session=False)
        db.delete(db_movie)
        db.commit()
        logger.info(f"Movie deleted with ID: {movie_id}")
        return db_movie
    logger.warning(f"Movie not found with ID: {movie_id}")
    return None
