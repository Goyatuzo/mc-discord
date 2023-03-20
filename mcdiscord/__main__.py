import discord 

from os import environ
from dotenv import load_dotenv
from discord.ext import tasks

# Load environment variables
load_dotenv(verbose=True)

from .graph import line_graph_single_stats, line_graph_distance_traveled
from .schedule.player_sync import player_sync 
from .servernet import setup


class McClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	async def setup_hook(self) -> None:
		self.player_sync.start()

	@tasks.loop(minutes=15)
	async def player_sync(self):
		player_sync()

	async def on_ready(self):
		print('Bot is ready')

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

intents = discord.Intents.default()
client = McClient(intents=intents)

setup()
client.run(environ['MCD_BOT_TOKEN'])