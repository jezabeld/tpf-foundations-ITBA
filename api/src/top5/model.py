from db.postgres import PostgresDB, get_db_status
from psycopg2.extras import RealDictCursor
from flask import current_app, jsonify
import sys
import time

def find_topcases():
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)
    cur = PostgresDB().get_connection().cursor(cursor_factory=RealDictCursor)

    query = """ SELECT  l.location,
        cast( (cast(total_cases as float)/population * 1000000) as int) as casesPerMillon
        FROM ( SELECT distinct iso_code,
                first_value(total_cases ) over (partition by iso_code order by date desc) as total_cases
                FROM daily_stats) t
        LEFT JOIN locations l
        on l.iso_code = t.iso_code 
        order by casesPerMillon desc
        limit 5
        """
    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    records = jsonify(records)
    return records 

def find_topvaccinated():
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)
    cur = PostgresDB().get_connection().cursor(cursor_factory=RealDictCursor)

    query = """ SELECT  l.location,
            case when people_vaccinated > population then 100 else cast( (cast(people_vaccinated as float)/population * 100) as int) end as porcVaccinated
            FROM ( SELECT distinct iso_code,
                    first_value(people_vaccinated ) over (partition by iso_code order by date desc) as people_vaccinated
                    FROM daily_stats) t
            LEFT JOIN locations l
            on l.iso_code = t.iso_code 
            order by porcVaccinated desc
            limit 5
            """
    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    records = jsonify(records)
    return records

def find_topvaccines():
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)
    cur = PostgresDB().get_connection().cursor(cursor_factory=RealDictCursor)

    query = """ select manufacturer, 
            sum(total_vaccinations) as total_vaccinations
            from (select distinct location, 
                manufacturer, 
                first_value(total_vaccinations) over (partition by location, manufacturer order by date desc) as total_vaccinations  
                from vaccines
            ) t 
            group by manufacturer 
            order by 2 desc
            limit 5
            """
    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    records = jsonify(records)
    return records 

def find_topkpi():
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)
    cur = PostgresDB().get_connection().cursor(cursor_factory=RealDictCursor)

    query = """ SELECT  l.location,
            total_cases,
            total_vaccinations,
            population,
            round( (case when total_vaccinations != 0 and total_cases != 0 then cast(total_cases as float)/total_vaccinations end)::numeric, 3) as KPI
            FROM ( SELECT distinct iso_code,
                    first_value(total_cases ) over (partition by iso_code order by date desc) as total_cases,
                    first_value(total_vaccinations ) over (partition by iso_code order by date desc) as total_vaccinations
                    FROM daily_stats) t
            LEFT JOIN locations l
            on l.iso_code = t.iso_code 
            order by KPI 
            limit 5
            """
    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    records = jsonify(records)
    return records 
