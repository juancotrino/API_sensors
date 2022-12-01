from typing import TYPE_CHECKING, List
from fastapi import FastAPI, Depends
import uvicorn
from datetime import datetime as dt

from sqlalchemy.orm import Session

import schema
import api_services
import database_services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


"""
It is assumed that:
    - The sensors won't fail in sending data to the API.
    - The measurements are delivered to the API at least every minute.
    - The data sent by the sensors will have resolution of 1 minute, no less.
    - The maximum resolution that the user can input for the time parameters is 1 minute.
    - One sensor is capable to take multiple types of measurements (parameters).
    - The user will always chose a time window available on the database.
"""


# Creating the API
app = FastAPI()


# Root endpoint
@app.get('/')
async def root():
    return {'Message': 'This is the root directory'}


# Endpoint for writing data into the database
@app.post('/measurements/{parameter}/', response_model=schema.WriteRecord)
async def write_to_db(parameter: str,
                      input_data: schema.WriteRecord,
                      db: Session = Depends(database_services.get_db)):
    return await api_services.write_data_from_sensor(parameter=parameter,
                                                     input_data=input_data,
                                                     db=db)


# Endpoint for retrieving data from database
@app.get('/measurements/{parameter}/', response_model=List[schema.RetrieveData])
async def retrieve_from_db(parameter: str,
                           sensor_id: str,
                           aggregation_time: int,
                           datetime_from: dt,
                           datetime_to: dt,
                           db: Session = Depends(database_services.get_db)):
    query = dict(parameter = parameter,
                 sensor_id = sensor_id,
                 aggregation_time = aggregation_time,
                 datetime_from = datetime_from.replace(second=0, microsecond=0),
                 datetime_to = datetime_to.replace(second=0, microsecond=0))
    return await api_services.retrieve_data(query=query,
                                            db=db)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
