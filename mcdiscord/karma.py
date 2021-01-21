from discord import Message

from .db import karma_collection

def karma_handler(message: Message) -> None:
	if message.content.endswith("++"):
		__add_karma(message.content[:-2])
	elif message.content.endswith("--"):
		__remove_karma(message.content[:-2])


def __add_karma(text: str) -> None:
	try:
		karma_collection.find_one_and_update({ "term": text }, {
				"$inc": { "plus": 1 }
			}, upsert=True)
	except Exception as e:
		print(e)


def __remove_karma(text: str) -> None:
	try:
		karma_collection.find_one_and_update({ "term": text }, {
				"$inc": { "minus": 1 }
			}, upsert=True)
	except Exception as e:
		print(e)

