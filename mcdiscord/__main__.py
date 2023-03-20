import discord 

from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True)

from .schedule import setup_schedule
from .servernet import setup
from .graph import line_graph_single_stats, line_graph_distance_traveled

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	setup()
	setup_schedule()
	print('Bot is ready')


@client.event
async def on_message(message: discord.Message):
	# If a message was send NOT from this bot
	if message.author.id != client.user.id:
		if message.content.startswith("!graph"):
			help_text = "Options are: killer, scrub"
			try:
				# First content is always command, so irrelevant
				_, graph_type = message.content.split()

				print(graph_type)

				if graph_type == 'killer':
					image_file = line_graph_single_stats("killed", y_axis_label="Kills")
					await message.channel.send(file=discord.File(image_file))
				# elif graph_type == "explorer":
				# 	image_file = line_graph_distance_traveled()
				# 	await message.channel.send(file=discord.File(image_file))
				elif graph_type == "scrub":
					image_file = line_graph_single_stats("killed_by", y_axis_label="Deaths")
					await message.channel.send(file=discord.File(image_file))
				else:
					await message.channel.send(help_text)
			# Errors if user doesn't type in a graph type so capture and send help text
			except Exception as e:
				print(e)
				await message.channel.send(help_text)
				await message.channel.send("Valid Commands: !graph")

client.run(environ['MCD_BOT_TOKEN'])
