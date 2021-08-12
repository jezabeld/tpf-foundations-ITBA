from db.postgres import PostgresDB, get_db_status
from psycopg2.extras import RealDictCursor
from flask import current_app, jsonify
import sys
import time

def find_global():
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)
    cur = PostgresDB().get_connection().cursor(cursor_factory=RealDictCursor)

    query = """ select manufacturer, 
            sum(total_vaccinations) as total_vaccinations, 
            count(distinct location) as countries 
            from (select distinct location, 
                manufacturer, 
                first_value(total_vaccinations) over (partition by location, manufacturer order by date desc) as total_vaccinations  
                from vaccines
            ) t 
            group by manufacturer 
            """
    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    records = jsonify(records)
    return records 