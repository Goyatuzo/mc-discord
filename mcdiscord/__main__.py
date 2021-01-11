import discord 
import matplotlib.pyplot as plt 
from os import environ
from dotenv import load_dotenv
from pathlib import Path
from operator import attrgetter

from .servernet import setup
from .players import Player

# The .env file should live in the parent directory
load_dotenv(dotenv_path=Path('../'))

client = discord.Client()

@client.event
async def on_ready():
	setup()

	print('Bot is ready')


@client.event
async def on_message(message):
	if message.content == '!killer':
		players = Player.get_all_players()
		players_by_lethality = sorted(players, key=attrgetter('total_mob_kills'), reverse=True)


		for player in players_by_lethality:
			plot = plt.bar([0], player.total_mob_kills)
			plot.set_label(player.username[1:] if player.username.startswith("_") else player.username)


		plt.legend()
		plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom= False)
		plt.savefig('killer.png')
		plt.clf()

		await message.channel.send(file=discord.File('killer.png'))


client.run(environ['MCD_BOT_TOKEN'])