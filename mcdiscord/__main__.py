import discord 
import matplotlib.pyplot as plt 
import pandas as pd

from os import environ
from dotenv import load_dotenv
from pathlib import Path
from operator import attrgetter

from .schedule import setup_schedule
from .servernet import setup
from .players import Player

from .db import stats_collection

# The .env file should live in the parent directory
load_dotenv(dotenv_path=Path('../'))

client = discord.Client()

@client.event
async def on_ready():
	setup()
	setup_schedule()

	print('Bot is ready')


@client.event
async def on_message(message):
	if message.content == '!killer':
		plt.clf()

		dat = pd.DataFrame(list(stats_collection.aggregate([{
				"$lookup": {
					"from": 'players',
					"localField": 'user_id',
					"foreignField": 'user_id',
					"as": 'player'
				}
			}, 
			{
				"$project": {
					"_id": 0,
					"name": { "$arrayElemAt":  ["$player.name", 0] },
					"date": 1,
					"kills": "$stat.mobKills._stat"
				}
			}
		])))

		dat["name"] = dat["name"].map(lambda name: name.lstrip("_") if name.startswith("_") else name)


		plt.figure()
	#	dat.set_index('date')['kills'].plot()
		dat.pivot(index="date", columns="name", values="kills").plot()
		
		plt.xlabel("Date")
		plt.ylabel("Kills")
		plt.savefig('killer.png')

		await message.channel.send(file=discord.File('killer.png'))


client.run(environ['MCD_BOT_TOKEN'])