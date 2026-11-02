from fastapi import FastAPI

app = FastAPI(
    title="Notes API",
    description="A shared notes service for capturing quick technical notes, decisions, and links.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Notes API"}
