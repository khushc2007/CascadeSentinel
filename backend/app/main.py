"""Minimal FastAPI entry point for the backend scaffold."""
from fastapi import FastAPI

app = FastAPI(title="Grid Doomsday Finder API")

@app.get("/health")
def health() -> dict[str, str]:
    """Confirm that the API process is available."""
    return {"status": "ok"}
