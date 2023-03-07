from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class Item(BaseModel):
    id: Optional[str]
    name: str
    price: Decimal
