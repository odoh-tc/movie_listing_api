from fastapi import FastAPI
from app.middlewares.auth_middleware import AuthMiddleware
from app.middlewares.cors_middleware import add_cors_middleware
from app.middlewares.error_handling_middleware import ErrorHandlingMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from slowapi.middleware import SlowAPIMiddleware


def setup_middlewares(app: FastAPI):
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(AuthMiddleware, excluded_paths=["/", "/docs", "/openapi.json", "/auth/login", "/auth/register/"])
    app.add_middleware(SlowAPIMiddleware)
    add_cors_middleware(app)
