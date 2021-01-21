from discord import Message

from .db import karma_collection

def karma_for_term(term: str) -> str:
	try:
		found = karma_collection.find_one({ "term": term })
		return f"{term}: {found['plus'] - found['minus']}, {found['plus']}++, {found['minus']}--"
	except Exception as ex:
		return f"{term} was not found"

def karma_handler(message: Message) -> None:
	if message.author.bot:
		_, msg = message.content.split(": ")
	else:
		msg = message.content

	if msg.endswith("++"):
		__add_karma(msg[:-2])
	elif message.content.endswith("--"):
		__remove_karma(msg[:-2])


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

