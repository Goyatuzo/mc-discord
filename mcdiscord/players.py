from typing import List
from os import listdir
from .servernet import get_server_file

def grab_user_ids() -> List[str]:
	player_folder = get_server_file("world", "playerdata", "gamestages")

	__uuid_cache = [f[:-4] for f in listdir(player_folder)]

	return __uuid_cache