import matplotlib.pyplot as plt
import pandas as pd

from .db import stats_collection

def line_graph_stats(*stat_key: str, y_axis_label="") -> str:
	plt.clf()

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
				"kills": f"$stat.{'.'.join(stat_key)}._stat"
			}
		}
	])))

	dat["name"] = dat["name"].map(lambda name: name.lstrip("_") if name.startswith("_") else name)


	plt.figure()
	dat.pivot(index="date", columns="name", values="kills").plot()
	
	plt.xlabel("Date")
	plt.ylabel(y_axis_label)
	plt.savefig('killer.png')

	return "killer.png"