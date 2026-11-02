"""Custom exception handlers to standardize error responses across the API.

All error responses strictly adhere to the required format:
{
  "error": "...",
  "message": "...",
  "field": null / "field_name",
  "detail": "..." (optional)
}
Every error is logged with its context (method, path, cause).
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import NoteNotFoundError
from app.logging_config import logger
from app.models.error import ErrorResponse


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on the FastAPI application."""

    @app.exception_handler(NoteNotFoundError)
    async def note_not_found_handler(request: Request, exc: NoteNotFoundError):
        logger.warning(
            "Note not found during %s %s: %s",
            request.method,
            request.url.path,
            exc,
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                error="note_not_found",
                message=str(exc),
                field=None,
            ).to_dict(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()

        # Handle malformed JSON request bodies as 400 Bad Request
        for err in errors:
            if err.get("type") == "json_invalid":
                logger.warning(
                    "Malformed JSON body received during %s %s",
                    request.method,
                    request.url.path,
                )
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=ErrorResponse(
                        error="bad_request",
                        message="Malformed JSON body",
                        field=None,
                    ).to_dict(),
                )

        first_err = errors[0] if errors else {}
        loc = first_err.get("loc", ())
        fields = [str(x) for x in loc if x != "body"]
        field = fields[0] if fields else None
        detail = first_err.get("msg", "Invalid input")

        logger.warning(
            "Validation failed during %s %s: field='%s', detail='%s'",
            request.method,
            request.url.path,
            field,
            detail,
        )

        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error="validation_error",
                message="Invalid input",
                field=field,
                detail=detail,
            ).to_dict(),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            error_code = "note_not_found"
        elif exc.status_code == status.HTTP_400_BAD_REQUEST:
            error_code = "bad_request"
        elif exc.status_code == 422:
            error_code = "validation_error"
        else:
            error_code = "http_error"

        message = exc.detail if isinstance(exc.detail, str) else "An error occurred"
        logger.warning(
            "HTTP %s during %s %s: %s",
            exc.status_code,
            request.method,
            request.url.path,
            message,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=error_code,
                message=message,
                field=None,
            ).to_dict(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception(
            "Unhandled exception during %s %s: %s",
            request.method,
            request.url.path,
            exc,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error="internal_server_error",
                message="Internal server error",
                field=None,
            ).to_dict(),
        )
