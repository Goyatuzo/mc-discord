import discord 
from os import environ
from dotenv import load_dotenv
from pathlib import Path
from mcstatus import MinecraftServer
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
	if message.content == '!players':
		server = MinecraftServer(environ['MC_SERVER_IP'], 25565)
		query = server.query()

		await message.channel.send(f"Players Online: {', '.join(query.players.names)}")
	elif message.content == '!killer':
		players = Player.get_all_players()
		players_by_lethality = sorted(players, key=attrgetter('total_mob_kills'), reverse=True)

		top_three = players_by_lethality[:3]
		to_respond = "\n".join([f"{player.username}: {player.total_mob_kills} mobs" for player in top_three])
	
		await message.channel.send(to_respond)

client.run(environ['MCD_BOT_TOKEN'])