from pydantic import BaseModel
from typing import Optional

class Car(BaseModel):
    id: Optional[int]
    model: str
    manufacturer: str
    year: int
    price: float
