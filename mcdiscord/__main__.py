import discord 

from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True)

from .schedule import setup_schedule
from .servernet import setup
from .graph import line_graph_single_stats, line_graph_distance_traveled
from .karma import karma_handler, karma_for_term

client = discord.Client()

@client.event
async def on_ready():
	setup()
	setup_schedule()
	print('Bot is ready')


@client.event
async def on_message(message: discord.Message):
	# If a message was send NOT from this bot
	if message.author.id != client.user.id:
		if message.content.startswith("!"):
			if message.content.startswith("!graph"):
				help_text = "Options are: killer, explorer, scrub, tank"
				try:
					# First content is always command, so irrelevant
					_, graph_type = message.content.split()

					if graph_type == 'killer':
						image_file = line_graph_single_stats("mobKills", y_axis_label="Kills")
						await message.channel.send(file=discord.File(image_file))
					elif graph_type == "explorer":
						image_file = line_graph_distance_traveled()
						await message.channel.send(file=discord.File(image_file))
					elif graph_type == "scrub":
						image_file = line_graph_single_stats("deaths", y_axis_label="Deaths")
						await message.channel.send(file=discord.File(image_file))
					elif graph_type == "tank":
						image_file = line_graph_single_stats("damageTaken", y_axis_label="Damage Taken")
						await message.channel.send(file=discord.File(image_file))
					else:
						await message.channel.send(help_text)
				# Errors if user doesn't type in a graph type so capture and send help text
				except:
					await message.channel.send(help_text)
			else:
				await message.channel.send("Valid Commands: !graph, !karma")

client.run(environ['MCD_BOT_TOKEN'])
