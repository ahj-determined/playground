import matplotlib.pyplot as plt
from collections import defaultdict
import pprint as pp
import numpy as np
import seaborn as sns

sns.set_style("darkgrid")

## REMINDER: REMOVE ADDITIONAL COMMAS IN WEBSITE DATA

def plot(data_path):

    # Get users of interest
    users_path = "data/results-usersgone.csv"
    users_of_interest = []
    start = False
    for line in open(users_path):
        if start:
            values = line.rstrip().split(",")
            users_of_interest.append(values[0])
        start = True

    # For each user, record what days they are up.
    start = False
    uptime_by_user = defaultdict(list)
    for line in open(data_path):
        if start:
            values = line.rstrip().split(",")
            user = values[0]
            date = values[1]
            uptime_by_user[user].append(date)
        start = True

    num_users_of_interest_are_whales = 0

    user_of_interest = "a976beda-adf2-4fa7-8176-d9ad1f70126d"
    lifetime_of_interest = []

    uptimes = []
    print("Num clusters: ", len(uptime_by_user.keys()))
    for user_id, uptime in uptime_by_user.items():
        uptimes.append(len(uptime))

        # Check which users are recurring
        if len(uptime) > 10:
            # Check which recurring users had left
            if user_id in users_of_interest:
                num_users_of_interest_are_whales += 1

        # Check on user of interest
        if user_id == user_of_interest:
            lifetime_of_interest = uptime

    print("Number of heavy hitters that left: {}/{}".format(num_users_of_interest_are_whales, len(users_of_interest)))

    kwargs = {'cumulative': True}
    bins = range(0, max(uptimes), 5)
    sns.distplot(np.asarray(uptimes), hist_kws=kwargs, kde_kws=kwargs, bins=bins)
    plt.xlabel("Days Up over Last 3 Months")
    plt.ylabel("Fraction of Clusters")
    plt.show()

    pp.pprint(lifetime_of_interest)


if  __name__ == "__main__":
    data_path = "data/results-ticks-userid-day.csv"

    plot(data_path)

