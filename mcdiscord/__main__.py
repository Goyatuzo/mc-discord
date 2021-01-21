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
	print(client)


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

			elif message.content.startswith("!karma"):
				try:
					msg = karma_for_term(message.content.split()[1])
					await message.channel.send(msg)
				except:
					await message.channel.send("Usage: !karma <term>")
			else:
				await message.channel.send("Valid Commands: !graph, !karma")
		# If a bot is sending the message, try some additional parsing
		elif message.author.bot:
			# MChat has format of user: message so remove user
			_, content = message.content.split(": ")

			if content.startswith("!karma"):
				try:
					msg = karma_for_term(content.split()[1])
					await message.channel.send(msg)
				except:
					await message.channel.send("Usage: !karma <term>")
			else:
				karma_handler(message)
		else:
			karma_handler(message)


client.run(environ['MCD_BOT_TOKEN'])
