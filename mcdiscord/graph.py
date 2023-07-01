import matplotlib.pyplot as plt
import pandas as pd

from time import time
from datetime import datetime

from .db import conn

# from .db import stats_collection

def __generate_graph_and_name(project_value: str, y_axis_label: str, fname: str="") -> str:
	# Start timing
	start_time = time()
	print(f"Graphing: {y_axis_label}")

	query = f"SELECT a.name, a.date, SUM(j.value) value FROM (PlayerStats t INNER JOIN Players p ON p.uuid = t.userId) a, json_each(json_extract(stats, '${project_value}')) j GROUP BY a.userId, a.date"

	# dat = pd.DataFrame([{ "name": res[0], "date": datetime.strptime(res[1], '%Y-%m-%dT%H:%M:%S.000Z'), "value": res[2]} for res in qu.fetchall()])
	dat = pd.read_sql_query(query, conn)

	print(dat.head())

	# Usernames that start with underscore break matplotlib, string escape yielded mixed results
	dat["name"] = dat["name"].map(lambda name: name.lstrip("_") if name.startswith("_") else name)
	dat["date"] = pd.to_datetime(dat["date"])

	# Begin constructing the graph
	plt.figure()

	# pandas gives an easier way of constructing a basic line graph
	dat.pivot(index="date", columns="name", values="value").plot()
	
	# # Set the labels accordingly
	plt.xlabel("Date")
	plt.ylabel(y_axis_label)

	# Move the legend outside of the graph
	plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

	# Finally save output file to system so Discord.py can send it
	output_filename = f'{fname}.png'
	plt.savefig(output_filename, bbox_inches='tight')

	print(f"Graphing: {y_axis_label} took {time() - start_time} seconds")

	# Clear the figure but keep window open for performance
	plt.clf()

	return output_filename

def line_graph_single_stats(stat_key: str, y_axis_label="") -> str:
	return __generate_graph_and_name(stat_key, y_axis_label, y_axis_label)

def line_graph_distance_traveled() -> str:
	# stats_cursor = stats_collection.find()

	# # Store all keys in unordered list to be uniqed via frozenset
	# distance_keys = []
	# for s in stats_cursor:
	# 	distance_keys += [stat for stat in s['stat'].keys() if stat.endswith("OneCm")]

	# uniq_distance_keys = frozenset(distance_keys)

	# # Convert the above list into Mongo fields to add
	# mongo_fields = [{'$ifNull': [ f"$stat.{field}._stat", 0 ]} for field in uniq_distance_keys]

	# return __generate_graph_and_name({
	# 	"$add": mongo_fields 
	# }, "Distance Traveled", "distance")
	pass
