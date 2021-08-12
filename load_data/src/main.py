from etl.import_data import get_new_stats, get_new_vaccines
from db.model import insert_locations, insert_stats, insert_vaccines, get_db_status
import sys
import logging


logging.basicConfig(level=logging.INFO, format='')

new_stats = get_new_stats()
new_vaccines = get_new_vaccines()

logging.debug('Load new countries:', len(new_stats['new_countries']))
insert_locations(new_stats['new_countries'])

logging.debug('Load new stats: ', len(new_stats['new_stats']))
insert_stats(new_stats['new_stats'])

logging.debug('Load new vaccines: ', len(new_vaccines))
insert_vaccines(new_vaccines)

print( "[Data Loader] Finishing...", file=sys.stderr)