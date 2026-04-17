from pydantic import BaseModel, ConfigDict


class ParcelTypeResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
