
from pydantic import BaseModel


class Cords(BaseModel):
    lat: str
    lon: str
