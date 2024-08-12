from fastapi import APIRouter
from app.routers import auth, movie, rating, comment, user
from app.utils.welcome_page import welcome_router


api_version = APIRouter(prefix="")

api_version.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_version.include_router(user.router, prefix="/users", tags=["user-management"])
api_version.include_router(movie.router, prefix="/movies", tags=["movie-catalog"])
api_version.include_router(rating.router, prefix="/ratings", tags=["rating-system"])
api_version.include_router(comment.router, prefix="/comments", tags=["commentary"])
api_version.include_router(welcome_router)
