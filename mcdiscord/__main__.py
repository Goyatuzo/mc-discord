import discord 
from os import environ
from dotenv import load_dotenv
from pathlib import Path

# The .env file should live in the parent directory
load_dotenv(dotenv_path=Path('../'))

client = discord.Client()

@client.event
async def on_ready():
	print('Bot is ready')

@client.event
async def on_message(message):
	pass

client.run(environ['MCD_BOT_TOKEN'])