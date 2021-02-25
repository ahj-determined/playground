import matplotlib.pyplot as plt
from collections import defaultdict
import pprint as pp
import numpy as np
import seaborn as sns

sns.set_style("darkgrid")

## REMINDER: REMOVE ADDITIONAL COMMAS IN WEBSITE DATA

def plot(users_path, metadata_path):

    # Get users of interest
    users_of_interest = []
    start = False
    for line in open(users_path):
        if start:
            values = line.rstrip().split(",")
            users_of_interest.append(values[0])
        start = True

    # Get metadata about users of interest
    start = False
    versions = {}
    for line in open(metadata_path):
        if start:
            values = line.rstrip().split(",")
            user = values[11]
            version = values[6]
            if user in users_of_interest:
                versions[user] = version
        start = True

    # Count versions
    version_counts = defaultdict(int)
    for u, v in versions.items():
        version_counts[v] += 1

    pp.pprint(version_counts)


if  __name__ == "__main__":
    metadata_path = "data/results-identifies-allusers.csv"
    users_path = "data/results-userscame.csv"
    users_path = "data/results-usersgone.csv"

    plot(users_path, metadata_path)

