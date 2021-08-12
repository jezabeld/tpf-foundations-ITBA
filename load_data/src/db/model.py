from db.postgres import PostgresDB
from io import StringIO
import time

# status
def get_db_status():
    cur = PostgresDB().get_cursor()
    query="""SELECT table_name
        FROM information_schema.tables 
        WHERE table_schema = 'public' """
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    records = [item for t in records for item in t]
    tables = ['locations', 'daily_stats','vaccines']
    if set(tables).issubset(set(records)):
        return True
    else:
        return False

# GET functions
def get_countries():
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)

    cur = PostgresDB().get_cursor()
    query = """ SELECT iso_code from locations """

    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    #return ['AFG','DZA']
    records = [item for t in records for item in t]
    return records

def get_stats_date():
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)

    cur = PostgresDB().get_cursor()
    query = """ SELECT iso_code, max(date) from daily_stats group by iso_code """

    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    records = {key: value for key, value in records}
    #return {'AFG': '2021-02-22', 'DZA': '2020-02-22'}
    return records

def get_vaccines_date():
    while not get_db_status():
        print('Waiting for table creation. Reatempting in 5 secs...')
        time.sleep(5)

    cur = PostgresDB().get_cursor()
    query = """ SELECT location, max(date) from vaccines group by location """

    # execute the Query and retrieve the records from the database
    cur.execute(query)
    records = cur.fetchall()
    cur.close()
    records = {key: value for key, value in records}
    #return {'Austria': '2021-01-29', 'Belgium': '2021-01-29'}ç
    return records


# INSERT functions
def insert_stats(new_data):
    if new_data:
        statsList= ""
        # generates a TSV (tab-separated file) with data to insert
        for row in new_data:
            statsList += f'{row.date}\t{row.iso_code}\t{row.total_cases}\t{row.new_cases}\t{row.total_deaths}\t{row.new_deaths}\t{row.total_tests}\t{row.new_tests}\t{row.new_vaccinations}\t{row.total_vaccinations}\t{row.people_vaccinated}\n'
        cur = PostgresDB().get_cursor()
        f = StringIO(statsList)
        # bulk insert
        cur.copy_from(f, 'daily_stats', null='None')
        PostgresDB().get_connection().commit()
        cur.close()
    
def insert_locations(new_data):
    if new_data:
        locationsList= ""
        # generates a TSV (tab-separated file) with data to insert
        for row in new_data:
            locationsList += f'{row.iso_code}\t{row.location}\t{row.continent}\t{row.population}\n'
        
        f = StringIO(locationsList)
        cur = PostgresDB().get_cursor()
        # bulk insert
        cur.copy_from(f, 'locations', null='None')
        PostgresDB().get_connection().commit()
        cur.close()

def insert_vaccines(new_data):
    if new_data:
        vaccinesList= ""
        # generates a TSV (tab-separated file) with data to insert
        for row in new_data:
            vaccinesList += f'{row.date}\t{row.location}\t{row.manufacturer}\t{row.total_vaccinations}\n'
        
        cur = PostgresDB().get_cursor()
        f = StringIO(vaccinesList)
        # bulk insert
        cur.copy_from(f, 'vaccines', null='None')
        PostgresDB().get_connection().commit()
        cur.close()