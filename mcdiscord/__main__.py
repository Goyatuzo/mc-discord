import discord 

from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True)

from .schedule import setup_schedule
from .servernet import setup
from .graph import line_graph_single_stats, line_graph_distance_traveled

client = discord.Client()

@client.event
async def on_ready():
	setup()
	setup_schedule()

	print('Bot is ready')


@client.event
async def on_message(message):
	if message.content == '!killer':
		image_file = line_graph_single_stats("mobKills", y_axis_label="Kills")
		await message.channel.send(file=discord.File(image_file))
	elif message.content == "!explorer":
		image_file = line_graph_distance_traveled()
		await message.channel.send(file=discord.File(image_file))


client.run(environ['MCD_BOT_TOKEN'])
