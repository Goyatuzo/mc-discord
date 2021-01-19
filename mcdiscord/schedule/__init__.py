import asyncio

from .stats import store_stats_in_database

loop = asyncio.get_event_loop()


def setup_schedule():
	loop.create_task(store_stats_in_database())