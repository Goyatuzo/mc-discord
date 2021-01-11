from pymongo import MongoClient
from os import environ 

db_client = MongoClient(environ['MC_BOT_DB_NAME'])

stats_collection = db_client['player_stats']