from db.postgres import PostgresDB, get_db_status
from psycopg2.extras import RealDictCursor
from flask import current_app, jsonify
import sys
import time

def find_global(date=None):
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)

    cur = PostgresDB().get_connection().cursor(cursor_factory=RealDictCursor)
    if(date == None):
        query = """ SELECT 'Global' as region,
                        count(iso_code) as countries,
                        max(date) as updated_at,
                        cast(sum(total_cases) as bigint) as total_cases,
                        cast(sum(total_deaths) as bigint) as total_deaths,
                        cast(sum(total_tests) as bigint) as total_tests,
                        cast(sum(total_vaccinations) as bigint) as total_vaccinations,
                        cast(sum(people_vaccinated) as bigint) as people_vaccinated
                    FROM ( SELECT distinct iso_code, 
                            first_value(date ) over (partition by iso_code order by date desc) as date,
                            first_value(total_cases ) over (partition by iso_code order by date desc) as total_cases,
                            first_value(total_deaths ) over (partition by iso_code order by date desc) as total_deaths,  
                            first_value(total_tests ) over (partition by iso_code order by date desc) as total_tests, 
                            first_value(total_vaccinations ) over (partition by iso_code order by date desc) as total_vaccinations, 
                            first_value(people_vaccinated ) over (partition by iso_code order by date desc) as people_vaccinated 
                        FROM daily_stats) t 
        """
    else:
        query = f""" SELECT 'Global' as region,
                        count(iso_code) as countries,
                        max(date) as updated_at,
                        cast(sum(total_cases) as bigint) as total_cases,
                        cast(sum(total_deaths) as bigint) as total_deaths,
                        cast(sum(total_tests) as bigint) as total_tests,
                        cast(sum(total_vaccinations) as bigint) as total_vaccinations,
                        cast(sum(people_vaccinated) as bigint) as people_vaccinated
                    FROM daily_stats
                    WHERE date = '{date}'
        """

    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    if (records):
        records = jsonify(records[0]) 
    else:
        records = None
    return records

def find_region(date, region):
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)
    cur = PostgresDB().get_connection().cursor(cursor_factory=RealDictCursor)
    if(date == None):
        if(len(region)>3):
            query = f""" SELECT continent as region,
                        count(iso_code) as countries,
                        max(date) as updated_at,
                        cast(sum(total_cases) as bigint) as total_cases,
                        cast(sum(total_deaths) as bigint) as total_deaths,
                        cast(sum(total_tests) as bigint) as total_tests,
                        cast(sum(total_vaccinations) as bigint) as total_vaccinations,
                        cast(sum(people_vaccinated) as bigint) as people_vaccinated
                    FROM ( SELECT distinct ds.iso_code, lc.continent,
                            first_value(date ) over (partition by ds.iso_code order by date desc) as date,
                            first_value(total_cases ) over (partition by ds.iso_code order by date desc) as total_cases,
                            first_value(total_deaths ) over (partition by ds.iso_code order by date desc) as total_deaths,  
                            first_value(total_tests ) over (partition by ds.iso_code order by date desc) as total_tests, 
                            first_value(total_vaccinations ) over (partition by ds.iso_code order by date desc) as total_vaccinations, 
                            first_value(people_vaccinated ) over (partition by ds.iso_code order by date desc) as people_vaccinated 
                        FROM daily_stats ds
                        LEFT JOIN locations lc
                            ON ds.iso_code = lc.iso_code
                        WHERE lower(lc.continent) = lower('{region}')
                    ) t 
                    GROUP BY continent
            """
        elif(len(region)==3):
            query = f""" SELECT location as region,
                        max(date) as updated_at,
                        cast(sum(total_cases) as bigint) as total_cases,
                        cast(sum(total_deaths) as bigint) as total_deaths,
                        cast(sum(total_tests) as bigint) as total_tests,
                        cast(sum(total_vaccinations) as bigint) as total_vaccinations,
                        cast(sum(people_vaccinated) as bigint) as people_vaccinated
                    FROM ( SELECT distinct ds.iso_code, lc.location,
                            first_value(date ) over (partition by ds.iso_code order by date desc) as date,
                            first_value(total_cases ) over (partition by ds.iso_code order by date desc) as total_cases,
                            first_value(total_deaths ) over (partition by ds.iso_code order by date desc) as total_deaths,  
                            first_value(total_tests ) over (partition by ds.iso_code order by date desc) as total_tests, 
                            first_value(total_vaccinations ) over (partition by ds.iso_code order by date desc) as total_vaccinations, 
                            first_value(people_vaccinated ) over (partition by ds.iso_code order by date desc) as people_vaccinated 
                        FROM daily_stats ds
                        LEFT JOIN locations lc
                            ON ds.iso_code = lc.iso_code
                        WHERE lower(ds.iso_code) = lower('{region}')
                    ) t 
                    GROUP BY location
            """
        else:
            return None
    else:
        if(len(region)>3):
            query = f""" SELECT lc.continent as region,
                            count(ds.iso_code) as countries,
                            max(date) as updated_at,
                            cast(sum(total_cases) as bigint) as total_cases,
                            cast(sum(total_deaths) as bigint) as total_deaths,
                            cast(sum(total_tests) as bigint) as total_tests,
                            cast(sum(total_vaccinations) as bigint) as total_vaccinations,
                            cast(sum(people_vaccinated) as bigint) as people_vaccinated
                        FROM daily_stats ds
                        LEFT JOIN locations lc
                            ON ds.iso_code = lc.iso_code
                        WHERE lower(lc.continent) = lower('{region}')
                            AND date = '{date}'
                        GROUP BY lc.continent
            """
        elif(len(region)==3):
            query = f""" SELECT lc.location as region,
                            max(date) as updated_at,
                            cast(sum(total_cases) as bigint) as total_cases,
                            cast(sum(total_deaths) as bigint) as total_deaths,
                            cast(sum(total_tests) as bigint) as total_tests,
                            cast(sum(total_vaccinations) as bigint) as total_vaccinations,
                            cast(sum(people_vaccinated) as bigint) as people_vaccinated
                        FROM daily_stats ds
                        LEFT JOIN locations lc
                            ON ds.iso_code = lc.iso_code
                        WHERE lower(ds.iso_code) = lower('{region}')
                            AND date = '{date}'
                        GROUP BY ds.iso_code, lc.location
            """
        else:
            return None

    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    if (records):
        records = jsonify(records[0]) 
    else:
        records = None
    return records 