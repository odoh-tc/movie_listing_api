from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from app.utils.logger import logger

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "status": False,
                    "status_code": exc.status_code,
                    "message": exc.detail,
                },
            )
        except ValidationError as exc:
            errors = []
            for error in exc.errors():
                loc = ' -> '.join([str(l) for l in error['loc']])
                msg = error['msg']
                errors.append(f"{loc}: {msg}")
            logger.error(f"Validation error: {errors}")
            return JSONResponse(
                status_code=422,
                content={
                    "status": False,
                    "status_code": 422,
                    "message": "Invalid input",
                    "errors": errors,
                },
            )
        except IntegrityError as exc:
            logger.exception(f"Exception occurred: {exc}")
            return JSONResponse(
                status_code=400,
                content={
                    "status": False,
                    "status_code": 400,
                    "message": "An unexpected error occurred: Integrity Error",
                },
            )
        except Exception as exc:
            logger.exception(f"Exception occurred: {exc}")
            return JSONResponse(
                status_code=500,
                content={
                    "status": False,
                    "status_code": 500,
                    "message": "An unexpected error occurred: Internal Server Error",
                },
            )
