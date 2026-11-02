from fastapi import FastAPI, Request

from app.handlers import register_exception_handlers
from app.logging_config import logger
from app.routes.notes import router as notes_router

app = FastAPI(
    title="Notes API",
    description="A shared notes service for capturing quick technical notes, decisions, and links.",
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every request: method, path, and status code.

    Request bodies are never logged to prevent exposing sensitive data.
    """
    response = await call_next(request)
    logger.info("%s %s %s", request.method, request.url.path, response.status_code)
    return response


# Register standardized error response handlers
register_exception_handlers(app)

# Include application routers
app.include_router(notes_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Notes API"}
