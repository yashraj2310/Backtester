from fastapi import FastAPI, HTTPException
from typing import List
from .database import db
from .models import TickerDataCreate, TickerDataResponse
from .strategy import moving_average_crossover_strategy
from fastapi import Query

app = FastAPI(
    title="Trading Data API",
    description="An API to fetch and add trading data, and run a simple strategy.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    if db.is_connected():
        await db.disconnect()

@app.get("/data", response_model=List[TickerDataResponse], tags=["Data"])
async def get_all_data():
    """
    Fetch all records from the database.
    """
    return await db.tickerdata.find_many(order={"datetime": "asc"})

@app.post("/data", response_model=TickerDataResponse, status_code=201, tags=["Data"])
async def add_new_data(data: TickerDataCreate):
    """
    Add a new data record to the database.
    Input data is validated using the TickerDataCreate Pydantic model.
    """
    try:
        
        new_record = await db.tickerdata.create(
            data=data.dict()  # type: ignore[reportArgumentType]
        )
        return new_record
    except Exception as e:
       
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Trading Data API. Visit /docs for more info."}


@app.get("/strategy/performance", tags=["Strategy"])
async def get_strategy_performance(
    short_window: int = Query(10, ge=1, description="Short-term moving average window."),
    long_window: int = Query(30, ge=1, description="Long-term moving average window.")
):
    """
    Calculates and returns the performance of a Moving Average Crossover strategy.
    
    Generates 'BUY' signals when the short-term MA crosses above the long-term MA,
    and 'SELL' signals when it crosses below.
    """
    if short_window >= long_window:
        raise HTTPException(
            status_code=400, 
            detail="The short_window must be less than the long_window."
        )

   
    all_data = await db.tickerdata.find_many(order={'datetime': 'asc'})
    
    
    data_dicts = [record.dict() for record in all_data]

   
    performance_results = moving_average_crossover_strategy(
        data_dicts, short_window, long_window
    )
    
    return performance_results
