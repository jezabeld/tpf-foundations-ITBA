import requests
import pandas as pd
import datetime as dt
from db.model import get_countries, get_stats_date, get_vaccines_date
import os
import sys
import logging

def string_to_date(string, fmt = "%Y-%m-%d"):
    if type(string) == str:
        return dt.datetime.strptime(string, fmt).date()
    elif type(string) == dt.date:
        return string

class Country:
    def __init__(self, iso_code, location, continent, population):
        self.iso_code = iso_code
        self.location = location
        self.continent = continent
        self.population = int(population) if population != None else 0

class DailyStats():
    def __init__(self, date, iso_code, total_cases, new_cases, total_deaths, new_deaths, total_tests, new_tests, new_vaccinations, total_vaccinations, people_vaccinated):
        self.date = date
        self.iso_code = iso_code
        self.total_cases = int(total_cases) if total_cases != None else 0
        self.new_cases = int(new_cases) if new_cases != None else 0
        self.total_deaths = int(total_deaths) if total_deaths != None else 0
        self.new_deaths = int(new_deaths) if new_deaths != None else 0
        self.total_tests = int(total_tests) if total_tests != None else 0
        self.new_tests = int(new_tests) if new_tests != None else 0
        self.new_vaccinations = int(new_vaccinations) if new_vaccinations != None else 0
        self.total_vaccinations = int(total_vaccinations) if total_vaccinations != None else 0
        self.people_vaccinated = int(people_vaccinated) if people_vaccinated != None else 0

class Vaccines:
    def __init__(self, location, date, manufacturer, total_vaccinations):
        self.date = date
        self.location = location
        self.manufacturer = manufacturer
        self.total_vaccinations = int(total_vaccinations) if total_vaccinations != None else 0

def get_new_stats():
    # get file URL from env var
    logging.info( "[Data Loader] Fetching stats file...")
    fileUrl = os.getenv('STATS_FILE')
    data = requests.get(fileUrl).json()
    
    logging.info( "[Data Loader] Fetching stats from db...")
    existing_countries = get_countries() 
    last_stats = get_stats_date() 
    
    # exclude grouped codes, not useful for this implementation
    excluded_codes = ['OWID_AFR', 'OWID_ASI','OWID_EUR','OWID_EUN','OWID_INT','OWID_KOS','OWID_NAM','OWID_CYN','OWID_OCE','OWID_SAM','OWID_WRL']
    
    new_countries = []
    new_stats = []
    
    logging.info( "[Data Loader] Comparing stats...")
    for key, val in data.items():
        # new locations
        if ((key not in existing_countries) & (key not in excluded_codes)):
            countryData = Country(key,val['location'], val['continent'], val['population'])
            new_countries.append(countryData)
        # new stats for existing countries
        if (key in list(last_stats.keys())):
            for stats in val['data']:
                if string_to_date(stats['date']) > string_to_date(last_stats[key]):
                    statsData = DailyStats(stats['date'],key,
                                           stats.get('total_cases',0), stats.get('new_cases',0),
                                           stats.get('total_deaths',0), stats.get('new_deaths',0),
                                           stats.get('total_tests',0), stats.get('new_tests',0),
                                           stats.get('new_vaccinations',0), stats.get('total_vaccinations',0),
                                           stats.get('people_vaccinated',0))
                    new_stats.append(statsData)
        # new stats for new countries
        elif ((key not in list(last_stats.keys())) & (key not in excluded_codes)):
                for stats in val['data']:
                    statsData = DailyStats(stats['date'],key,
                                           stats.get('total_cases',0), stats.get('new_cases',0),
                                           stats.get('total_deaths',0), stats.get('new_deaths',0),
                                           stats.get('total_tests',0), stats.get('new_tests',0),
                                           stats.get('new_vaccinations',0), stats.get('total_vaccinations',0),
                                           stats.get('people_vaccinated',0))
                    new_stats.append(statsData)
    
    d = {'new_countries': new_countries, 'new_stats': new_stats}   
    return d

def get_new_vaccines():
    # get file URL from env var
    logging.info( "[Data Loader] Fetching vaccines file...")
    fileUrl = os.getenv('VACCINES_FILE')
    data = pd.read_csv(fileUrl)
        
    logging.info( "[Data Loader] Fetching vaccines from db...")
    existing_vaccines = pd.DataFrame(list(get_vaccines_date().items()),columns=['location','last_date'])
    
    filtered_dataframe = data.merge(existing_vaccines, on=['location'], how='left')
    filtered_dataframe['date'] = pd.to_datetime(filtered_dataframe['date'], format="%Y-%m-%d")
    filtered_dataframe = filtered_dataframe[
        (filtered_dataframe['date'] > filtered_dataframe['last_date']) | (filtered_dataframe['last_date'].isnull())
    ]
    filtered_dataframe = filtered_dataframe.drop(columns=['last_date'])
    filtered_dataframe = filtered_dataframe.drop_duplicates(subset=["date","location","vaccine"], keep='last')
    
    logging.info( "[Data Loader] Comparing vaccines...")
    new_vaccines = []
    for index, row in filtered_dataframe.iterrows():
        vaccineData = Vaccines(row['location'], row['date'], row['vaccine'], row['total_vaccinations'])
        new_vaccines.append(vaccineData)
        
    return new_vaccines