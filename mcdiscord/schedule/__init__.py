import asyncio

from .stats import store_stats_in_database
from .players import store_players_in_database



def setup_schedule():
	loop = asyncio.get_event_loop()
	loop.create_task(store_stats_in_database())
	loop.create_task(store_players_in_database())
	loop.run_forever()