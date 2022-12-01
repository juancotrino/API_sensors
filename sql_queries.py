from datetime import timedelta
from datetime import datetime as dt

from sqlalchemy import func
from sqlalchemy import text


def execute_sql_query(table_name, query, db):

    sql_raw_query = text(f'''

    WITH

        -- Subquery to compute aggregative functions on the given aggregation time
        aggTable AS (
            SELECT
                FLOOR(date_part('minute', {table_name}.recorded_at)/{query['aggregation_time']}) AS bucket,
                MIN({table_name}.value),
                AVG({table_name}.value),
                MAX({table_name}.value)
            FROM {table_name}
            WHERE {table_name}.sensor_id = '{query['sensor_id']}'
                AND {table_name}.recorded_at BETWEEN '{query['datetime_from']}' AND '{query['datetime_to']}'
            GROUP BY date_trunc('hour', {table_name}.recorded_at), bucket
            ORDER BY bucket ASC
        ),

        -- Subquery to filter data on the sensor ID and the time frame chosen by the user
        filteredTable AS (
            SELECT
                {table_name}.sensor_id,
                {table_name}.recorded_at
            FROM {table_name}
            WHERE {table_name}.sensor_id = '{query['sensor_id']}'
                AND {table_name}.recorded_at <= '{query['datetime_to']}'
                AND {table_name}.recorded_at >= '{query['datetime_from']}'
        ),

        -- Subquery to generate dummy series of aggregation time selected by the user within the time frame
        bucketTable AS (
            SELECT
                generate_series(min(filteredTable.recorded_at),
                                max(filteredTable.recorded_at),
                                '{query['aggregation_time']} minutes'::interval)
            FROM filteredTable
        )

    -- Querey to combine previous tables
    SELECT
        t1.generate_series AS aggregated_timestamp,
        t2.min AS min_value,
        t2.avg AS mean_value,
        t2.max AS max_value
    FROM (
    SELECT *, ROW_NUMBER() OVER() AS rn FROM bucketTable
    ) AS t1
    FULL JOIN (
    SELECT *, ROW_NUMBER() OVER() AS rn FROM aggTable
    ) AS t2 ON t1.rn = t2.rn

    ''')

    aggregated_values = db.execute(sql_raw_query).all()

    # Not the best way to deal with this error
    if aggregated_values[-1][0] == None:
        del aggregated_values[-1]

    return aggregated_values
