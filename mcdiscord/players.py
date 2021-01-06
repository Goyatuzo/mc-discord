from typing import List
from os import listdir
from json import load as jload
from nbtlib import load as nload

from .servernet import get_server_file

class Player:
	__uuid: str
	__username: str

	def __init__(self, uuid):
		self.__uuid = uuid

	def load_data(self):
		fpath = get_server_file("usernamecache.json")

		with open(fpath, mode='r') as f:
			username_cache = jload(f)
			self.__username = username_cache[str(self.__uuid)]


	@property
	def username(self) -> str:
		return self.__username

	@staticmethod
	def get_all_user_ids() -> List[str]:
		player_folder = get_server_file("world", "playerdata", "gamestages")

		__uuid_cache = [f[:-4] for f in listdir(player_folder)]

		return __uuid_cache
