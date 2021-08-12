import psycopg2
import os
import atexit
import time

# helper class to return always existing connection to db
class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class PostgresDB(Singleton):
    connection = None
    
    def get_connection(self):
        if (self.connection != None):
            return self.connection

        # Get environment variables
        USER = os.getenv('DATABASE_USERNAME')
        PASSWORD = os.getenv('DATABASE_PASSWORD')
        DB_URL = os.getenv('DATABASE_URL')
        DB_NAME = os.getenv('DATABASE_NAME')

        try:
            self.connection = psycopg2.connect(
                host=DB_URL,
                database= DB_NAME,
                user= USER,
                password= PASSWORD)
            return self.connection

        except Exception as err:
            print(err)
            print('Reatempting connection to database...')
            
            time.sleep(10)
            return self.get_connection()

    def get_cursor(self):
        return self.get_connection().cursor()
        
    def close_connection(self):
        if (self.connection != None):
            self.connection.close()

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

def exit_handler():
    PostgresDB().close_connection()

atexit.register(exit_handler)