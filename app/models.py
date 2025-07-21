from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

# Model for creating a new record (input)
class TickerDataCreate(BaseModel):
    datetime: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int

# Model for representing a record from the DB (output)

class TickerDataResponse(TickerDataCreate):
    id: str

    class Config:
        orm_mode = True 