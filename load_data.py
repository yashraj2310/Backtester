import pandas as pd
from prisma import Prisma
from decimal import Decimal
import asyncio

async def main():
    db = Prisma()
    await db.connect()
    await db.tickerdata.delete_many()
    print("Cleared existing data.")

    df = pd.read_csv("data.csv", parse_dates=["datetime"])
    print(f"Read {len(df)} rows from CSV.")

    records_to_create = []
    for row in df.itertuples(index=False):
        records_to_create.append({
            "datetime": row.datetime,                   # pandas.Timestamp works as a datetime
            "open":     Decimal(str(row.open)),
            "high":     Decimal(str(row.high)),
            "low":      Decimal(str(row.low)),
            "close":    Decimal(str(row.close)),
            "volume":   int(row.volume),
        })

    await db.tickerdata.create_many(records_to_create)
    print(f"Successfully loaded {len(records_to_create)} records.")
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
