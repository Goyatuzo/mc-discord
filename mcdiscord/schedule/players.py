import asyncio
from json import loads
from sqlite3 import Connection

from ..servernet import get_server_file

async def store_players_in_database(connection: Connection):
	print("Obtained cursor")
	cursor = connection.cursor()
	
	print("Created Players DB")
	cursor.execute("CREATE TABLE IF NOT EXISTS Players (id VARCHAR(36), name VARCHAR(255));")

	# Periodically call the same method by looping indefinitely
	while True:
		fpath = get_server_file("usercache.json")

		users_to_process = []
		with open(fpath) as f:
			users = loads(f.read())

			for user in users:
				print(f"Updating id: {user['uuid']}, name: {user['name']} in DB")
				to_process = (
					user["uuid"],
					user["name"]
				)

				users_to_process.push(to_process)

		print(f"Processing {len(users_to_process)} ids to usernames")

		cursor.execute("INSERT OR REPLACE INTO Players (id, name) VALUES (?, ?)", users_to_process)



		# Run this in 30 minutes time
		await asyncio.sleep(1800)