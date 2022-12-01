from typing import TYPE_CHECKING, List
import importlib

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from fastapi import HTTPException

from parameters import PARAMETERS
import schema
from sql_queries import execute_sql_query


# Function for writing the data
async def write_data_from_sensor(parameter: str,
                                 input_data: schema.WriteRecord,
                                 db: "Session") -> schema.WriteRecord:

    # Checks what is the parameter the data is coming from
    parameter_name = check_parameter(parameter)

    # Get the class corresponding to the parameter chosen
    # Scalable when adding more Measurement Types to both 'models.py' and 'parameters.py' files
    parameter_class = class_for_name('models', parameter_name)

    # Unwrap the data
    input_data = parameter_class(**input_data.dict())

    # Drop seconds and miliseconds from the timestamp
    input_data.recorded_at = input_data.recorded_at.replace(second=0, microsecond=0)

    # Writes the data
    db.add(input_data)
    db.commit()
    db.refresh(input_data)

    return schema.WriteRecord.from_orm(input_data)


# Function for retrieving data
async def retrieve_data(query: dict,
                        db: "Session") -> List[schema.RetrieveData]:

    # Checks what is the parameter the data is coming from
    parameter_name = check_parameter(query['parameter'])

    # Get the class corresponding to the parameter chosen
    # Scalable when adding more Measurement Types
    parameter_class = class_for_name('models', parameter_name)
    table_name = parameter_class.__tablename__

    # Get aggregated values from SQL query
    response = execute_sql_query(table_name, query, db)
    print('The query was succesful...........')

    return list(map(schema.RetrieveData.from_orm, response))


# Checks the existence of the requested parameter
def check_parameter(parameter):
    if parameter not in PARAMETERS.values():
        raise HTTPException(status_code=404,
                            headers={"X-Error": 'Check parameter alias'},
                            detail={'Parameters available': PARAMETERS})

    for name, alias in PARAMETERS.items():
        if alias == parameter:
            parameter_name = name

    return parameter_name


# Function to convert a string to a class define in 'models' module, representing a parameter (e.g. Temperature)
def class_for_name(module_name, class_name):
    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    return c
