import asyncio
from json import loads

from ..db import player_collection 
from ..servernet import get_server_file

async def store_players_in_database():
	# Periodically call the same method by looping indefinitely
	while True:
		fpath = get_server_file("usercache.json")

		with open(fpath) as f:
			users = loads(f.read())

			for user in users:
				print(f"Updating {user['name']} in DB")
				to_insert = {
					"user_id": user["uuid"],
					"name": user["name"]
				}

				player_collection.update(to_insert, to_insert, upsert=True)


		# Run this in 30 minutes time
		await asyncio.sleep(1800)