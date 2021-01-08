from typing import List
from json import load as jload
from nbtlib import load as nload

from .servernet import get_server_file

class Player:
	__uuid: str
	__username: str

	def __init__(self, uuid, username):
		self.__uuid = uuid
		self.__username = username
		

	@property
	def username(self) -> str:
		return self.__username

	@property
	def total_mob_kills(self) -> int:
		"""Get the total amount of kills done by this player."""
		stats_file = get_server_file("world", "stats", f"{self.__uuid}.json")

		with open(stats_file, mode="r") as f:
			stats = jload(f)

		try:
			return stats['stat.mobKills']
		except:
			return 0

	@staticmethod
	def __load_username_cache() -> dict:
		fpath = get_server_file("usernamecache.json")

		with open(fpath, mode='r') as f:
			username_cache = jload(f)

		return username_cache

	@classmethod
	def get_all_players(cls):
		all_users = cls.__load_username_cache()
		return [cls(uuid, name) for uuid, name in all_users.items()]

	@classmethod
	def get_by_username(cls, username):
		"""Create a player class from a given username."""
		all_users = cls.__load_username_cache()

		for uuid, uname in all_users.items():
			if uname == username:
				return cls(uuid, uname)

		# If a user wasn't found, return an empty instance
		return cls(None, None)