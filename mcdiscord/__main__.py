import discord 

from .servernet import setup
setup()

from os import environ
from dotenv import load_dotenv
from discord.ext import tasks

# Load environment variables
load_dotenv(verbose=True)

from .graph import line_graph_single_stats, line_graph_distance_traveled
from .schedule import players
from .schedule import stats

class McClient(discord.Client):
	async def setup_hook(self) -> None:
		player_sync.start()
		player_stats_sync.start()


	async def on_ready(self):
		print('Bot is ready')

	async def on_message(self, message: discord.Message):
		# If a message was send NOT from this bot
		if message.author.id != client.user.id:
			if message.content.startswith("!graph"):
				help_text = "Options are: killer, scrub"
				try:
					# First content is always command, so irrelevant
					_, graph_type = message.content.split()

					print(graph_type)

					if graph_type == 'killer':
						image_file = line_graph_single_stats("minecraft:killed", y_axis_label="Kills")
						await message.channel.send(file=discord.File(image_file))
					# elif graph_type == "explorer":
					# 	image_file = line_graph_distance_traveled()
					# 	await message.channel.send(file=discord.File(image_file))
					elif graph_type == "scrub":
						image_file = line_graph_single_stats("minecraft:killed_by", y_axis_label="Deaths")
						await message.channel.send(file=discord.File(image_file))
					else:
						await message.channel.send(help_text)
				# Errors if user doesn't type in a graph type so capture and send help text
				except Exception as e:
					print(e)
					await message.channel.send(help_text)
					await message.channel.send("Valid Commands: !graph")


@tasks.loop(minutes=10)
async def player_sync():
	await players.store_players_in_database()

@tasks.loop(minutes=10)
async def player_stats_sync():
	await stats.store_stats_in_database()


intents = discord.Intents.default()
intents.message_content = True
client = McClient(intents=intents)

client.run(environ['MCD_BOT_TOKEN'])