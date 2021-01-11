from pymongo import MongoClient
from os import environ 

db_client = MongoClient(environ['MC_BOT_DB_NAME'])