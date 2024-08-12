# Import necessary modules and packages
from fastapi import FastAPI
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.middlewares.middleware_setup import setup_middlewares
from app.routers import api_version
from app.utils.logger import logger
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.utils.rate_limiter import limiter

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Movie Listing API",
    description="Welcome to the Movie Listing API! This API allows you to manage movies, including adding, viewing, updating, and deleting movies. Enjoy a seamless experience with our authentication, user management, and rating systems.",
    version="1.0.0",
)

# Include API routers and setup middlewares
app.include_router(api_version)
setup_middlewares(app)

# Setup rate limiter and exception handler for rate limit exceeded
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Startup event: Initialize the database and log startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

# Shutdown event: Log shutdown
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
