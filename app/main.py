from fastapi import FastAPI

from app.routes.notes import router as notes_router

app = FastAPI(
    title="Notes API",
    description="A shared notes service for capturing quick technical notes, decisions, and links.",
    version="1.0.0",
)

app.include_router(notes_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Notes API"}
