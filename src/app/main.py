from fastapi import FastAPI

from app.api.v1.parcels import router as parcels_router
import app.models

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


app.include_router(parcels_router)
