import discord 
from os import environ
from dotenv import load_dotenv
from pathlib import Path
from mcstatus import MinecraftServer
from .servernet import setup

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


client.run(environ['MCD_BOT_TOKEN'])