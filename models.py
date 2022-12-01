from datetime import datetime as dt
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base

# Creates base
Base = declarative_base()


# Main object of measurement
class Measurement():
    registry_id = sql.Column('registry_id', sql.Integer, primary_key=True, autoincrement=True)
    sensor_id = sql.Column('sensor_id', sql.String, index=True,
                           comment='Sensors ID')
    recorded_at = sql.Column('recorded_at', sql.DateTime, default=dt.utcnow().replace(second=0, microsecond=0),
                             comment='Timestamp when the value was recorded in the database')


# Temperature measurement object
class Temperature(Measurement, Base):
    __tablename__ = 'temperature_celsius'
    value = sql.Column('value', sql.Float, index=True,
                       comment='Temperature in degree Celsius')


# Reelative huminidty measurement object
class RelativeHumidity(Measurement, Base):
    __tablename__ = 'relative_humidity'
    value = sql.Column('value', sql.Float, index=True,
                       comment='Relative Humidity in percentage')
