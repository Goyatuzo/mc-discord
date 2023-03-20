from json import loads

from ..db import db_client
from ..servernet import get_server_file

def player_sync():
	cursor = db_client.cursor()
	
	cursor.execute("CREATE TABLE IF NOT EXISTS Players (id VARCHAR(36), name VARCHAR(255));")

	fpath = get_server_file("usercache.json")

	print(fpath)

	users_to_process = []
	with open(fpath) as f:
		users = loads(f.read())

		for user in users:
			to_process = (
				user["uuid"],
				user["name"]
			)

			users_to_process.append(to_process)

	cursor.executemany("INSERT OR REPLACE INTO Players (id, name) VALUES (?, ?)", users_to_process)
	db_client.commit()
