import asyncio
from zipfile import ZipFile
from os import listdir, path
from json import loads
from datetime import datetime

from ..db import stats_collection 
from ..servernet import get_server_file

async def store_stats_in_database():
	# Periodically call the same method by looping indefinitely
	while True:
		backups_folder = get_server_file("backups", "world")

		all_zips = [f for f in listdir(backups_folder) if f.endswith('.zip')]
		all_zips = sorted(all_zips)
		
		# Store the final data to be stored in DB
		data_by_date: dict = {}
		for fname in all_zips:
			# Grab fnames that have actual backup data
			print(f"Processing {fname} for stats")
			# The date to associate this particular data point with
			# The file is of the format Backup--world--DATE
			# So just ignore irrelevant strings including zip extension
			raw_date = fname[len('Backup--world--'):-11]
			parsed_date = datetime.strptime(raw_date, "%Y-%m-%d")

			with ZipFile(path.join(backups_folder, fname), 'r') as zf:

				# Could potentially break if some other stats folder comes into play.
				stats_fnames = [f for f in zf.namelist() if f.startswith(f"stats{path.sep}") and f.endswith(".json")]

				for stat_fname in stats_fnames:
					# Get the UUID of the user by parsing file name
					# Separate by folder delimitter and then remove json extension
					uniq_id = stat_fname.split(path.sep)[-1][:-5]

					f = zf.read(stat_fname)

					user_data = {
						"user_id": uniq_id,
						"date": parsed_date,
						"data": loads(f)
					}
					data_by_date[f"{parsed_date}{uniq_id}"] = user_data
					
				
		for v in data_by_date.values():
			mongo_key = {
				"user_id": v["user_id"],
				"date": v["date"]
			}

			print(f"Adding {v['user_id']} stats at {v['date']}")
			stats_collection.replace_one(mongo_key, v, upsert=True)

		# Run this in 30 minutes time
		await asyncio.sleep(1800)