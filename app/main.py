from fastapi import FastAPI

from app.handlers import register_exception_handlers
from app.routes.notes import router as notes_router

app = FastAPI(
    title="Notes API",
    description="A shared notes service for capturing quick technical notes, decisions, and links.",
    version="1.0.0",
)

# Register standardized error response handlers
register_exception_handlers(app)

# Include application routers
app.include_router(notes_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Notes API"}
