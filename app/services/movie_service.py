from sqlalchemy.orm import Session
from app.crud.crud_movie import create_movie, get_movie, get_movies, update_movie, delete_movie
from app.db.schemas.movie import MovieCreate, MovieUpdate, MovieResponse
from app.utils.logger import logger
from uuid import UUID

async def create_movie_service(db: Session, movie: MovieCreate, user_id: UUID) -> MovieResponse:
    logger.info("Service: Creating movie.")
    db_movie = create_movie(db, movie, user_id)
    logger.info("Service: Movie created successfully.")
    return MovieResponse.from_orm(db_movie)


async def get_movie_service(db: Session, movie_id: UUID) -> MovieResponse:
    logger.info(f"Service: Fetching movie with ID: {movie_id}")
    movie = get_movie(db, movie_id)
    if not movie:
        logger.warning("Service: Movie not found.")
        return None
    logger.info("Service: Movie found.")
    return MovieResponse.from_orm(movie)


async def get_movies_service(db: Session, skip: int = 0, limit: int = 10, search: str = None) -> list[MovieResponse]:
    logger.info("Service: Fetching movies list.")
    movies = get_movies(db, skip, limit, search)
    logger.info(f"Service: Retrieved {len(movies)} movies.")
    return [MovieResponse.from_orm(movie) for movie in movies]

async def update_movie_service(db: Session, movie_id: UUID, movie: MovieUpdate, user_id: UUID) -> MovieResponse:
    logger.info(f"Service: Updating movie with ID: {movie_id}")
    db_movie = get_movie(db, movie_id)
    if not db_movie:
        logger.warning(f"Movie not found with ID: {movie_id}")
        return None
    if db_movie.owner_id != user_id:
        logger.warning(f"Unauthorized update attempt for movie ID: {movie_id} by user ID: {user_id}")
        return None
    updated_movie = update_movie(db, movie_id, movie)
    logger.info("Service: Movie updated successfully.")
    return MovieResponse.from_orm(updated_movie)

async def delete_movie_service(db: Session, movie_id: UUID, user_id: UUID) -> bool:
    logger.info(f"Service: Deleting movie with ID: {movie_id}")
    db_movie = get_movie(db, movie_id)
    if not db_movie:
        logger.warning(f"Movie not found with ID: {movie_id}")
        return False
    if db_movie.owner_id != user_id:
        logger.warning(f"Unauthorized delete attempt for movie ID: {movie_id} by user ID: {user_id}")
        return False
    delete_movie(db, movie_id)
    logger.info("Service: Movie deleted successfully.")
    return True
