from pydantic import BaseModel
from datetime import datetime as dt

# Schema of the measurements
class WriteRecord(BaseModel):
    sensor_id: str
    recorded_at: dt
    value: float

    class Config:
        orm_mode = True


# Schema used when retrieving the data
class RetrieveData(BaseModel):
    aggregated_timestamp: dt
    min_value: float
    mean_value: float
    max_value: float

    class Config:
        orm_mode = True
