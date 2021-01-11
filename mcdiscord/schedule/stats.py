import asyncio
from zipfile import ZipFile
from os import listdir, path
from uuid import UUID

from ..db import stats_collection 
from ..servernet import get_server_file

async def store_stats_in_database():
	# Periodically call the same method by looping indefinitely
	while True:
		backups_folder = get_server_file("backups", "world")

		for fname in listdir(backups_folder):
			print(f"Processing {fname} for stats")
			if fname.endswith('.zip'):

				with ZipFile(path.join(backups_folder, fname), 'r') as zf:
					# Could potentially break if some other stats folder comes into play.
					stats_fnames = [f for f in zf.namelist() if f.startswith(f"stats{path.sep}") and f.endswith(".json")]

					for stat_fname in stats_fnames:
						# Get the UUID of the user by parsing file name
						# Separate by folder delimitter and then remove json extension
						uniq_id = UUID(stat_fname.split(path.sep)[-1][:-5])
						with zf.open(stat_fname, 'r') as stat_contents:
							print(stat_contents.name)


		stats_collection
		# Run this in 30 minutes time
		await asyncio.sleep(1800)