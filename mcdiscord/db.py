from pymongo import MongoClient
from os import environ 
from urllib import parse

db_client = MongoClient(environ['MC_BOT_MONGODB'])

db = db_client[environ['MC_BOT_DB_NAME']]

stats_collection = db['player_stats']
player_collection = db['players']
karma_collection = db['karma']