"""FastAPI application placeholder for the Taiwan 100 Peaks dashboard."""

from fastapi import FastAPI

from app.routers import dashboard, mountains


app = FastAPI(title="Taiwan 100 Peaks Dashboard API")

app.include_router(mountains.router)
app.include_router(dashboard.router)
