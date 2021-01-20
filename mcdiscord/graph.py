import matplotlib.pyplot as plt
import pandas as pd

from time import time

from .db import stats_collection

def __generate_graph_and_name(project_value: str, y_axis_label: str, fname: str="") -> str:
	# Start timing
	start_time = time()

	plt.clf()

	print(f"Graphing: {project_value}")
	dat = pd.DataFrame(list(stats_collection.aggregate([{
			"$lookup": {
				"from": 'players',
				"localField": 'user_id',
				"foreignField": 'user_id',
				"as": 'player'
			}
		}, 
		{
			"$project": {
				"_id": 0,
				"name": { "$arrayElemAt":  ["$player.name", 0] },
				"date": 1,
				"value": project_value
			}
		}
	])))

	# Usernames that start with underscore break matplotlib, string escape yielded mixed results
	dat["name"] = dat["name"].map(lambda name: name.lstrip("_") if name.startswith("_") else name)

	# Begin constructing the graph
	plt.figure()

	# pandas gives an easier way of constructing a basic line graph
	dat.pivot(index="date", columns="name", values="value").plot()
	
	# Set the labels accordingly
	plt.xlabel("Date")
	plt.ylabel(y_axis_label)

	# Finally save output file to system so Discord.py can send it
	output_filename = f'{fname}.png'
	plt.savefig(output_filename)

	print(f"Graphing: {project_value} took {time() - start_time} seconds")

	return output_filename

def line_graph_single_stats(*stat_key: str, y_axis_label="") -> str:
	return __generate_graph_and_name(f"$stat.{'.'.join(stat_key)}._stat", y_axis_label, y_axis_label)

def line_graph_distance_traveled() -> str:
	distance_stats = ["crouchOneCm",
						"flyOneCm",
						"diveOneCm",
						"walkOneCm",
						"runOneCm",
						"fallOneCm",
						"climbOneCm",
						"boatOneCm",
						"swimOneCm",
						"horseOneCm"]

	return __generate_graph_and_name({
		"$add": distance_stats
	}, "Distance Traveled", "distance")