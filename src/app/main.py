from fastapi import FastAPI

from app.api.v1.parcel_types import router as parcel_types_router
from app.api.v1.parcels import router as parcels_router
import app.models
from app.tasks.scheduler import start_scheduler

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    start_scheduler()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


app.include_router(parcels_router)
app.include_router(parcel_types_router)
