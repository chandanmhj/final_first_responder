"""Shared exceptions and their HTTP mapping."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for errors that should become a clean JSON response."""

    status_code = 400
    code = "bad_request"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class Unauthorized(AppError):
    status_code = 401
    code = "unauthorized"


class NotFound(AppError):
    status_code = 404
    code = "not_found"


class TooManyRequests(AppError):
    status_code = 429
    code = "rate_limited"


class UpstreamError(AppError):
    status_code = 502
    code = "upstream_error"


def install_error_handlers(app: FastAPI) -> None:
    """Register handlers so every error has the same JSON shape."""

    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError):
        return JSONResponse(status_code=exc.status_code, content={"error": exc.code, "message": exc.message})
