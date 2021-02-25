import time
import sys
from collections import Counter
import pprint as pp
import requests
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime


sns.set_style("darkgrid")

# Write text from channels to file
def get_slack_messages(auth_token, channel, num_historical_weeks, outfile="./text.txt"):
    seconds_in_a_week = 604800
    latest = time.time()
    oldest = latest - seconds_in_a_week

    week_of_times = []
    thread_counts = []
    all_text = ""

    with open(outfile, "w+") as f:
        for i in range(num_historical_weeks):
            params = {
                    "latest": latest,
                    "oldest": oldest, 
                    "limit": 1000,
                    }

            # API call
            r = requests.post("https://slack.com/api/conversations.history?channel={}&pretty=1".format(channel),
                              params = params,
                              headers = {"Authorization": "Bearer {}".format(auth_token)})

            # Check for errors
            if r.status_code != 200:
                print("ERROR: API returned Status {} due to {}".format(r.status_code, r.reason))
                exit()

            messages = r.json()["messages"]
            print("API returned {} messages".format(len(messages)))
            messages = [m for m in messages if "has joined the channel" not in m["text"]]
            for m in messages:
                all_text += m["text"].rstrip()
            latest = oldest
            oldest = latest - seconds_in_a_week

        '''
        words = all_text.split()
        my_counter = Counter(words)
        most_common = my_counter.most_common(500)
        for tup in most_common:
            k = tup[0]
            v = tup[1]
        '''
        line = "{}\n".format(all_text)
        f.write(line)


# Write number of slack threads by channel to outfile
def get_slack_history(auth_token, channel, num_historical_weeks, outfile="./out.txt"):
    seconds_in_a_week = 604800
    latest = time.time()
    oldest = latest - seconds_in_a_week

    week_of_times = []
    thread_counts = []

    with open(outfile, "w+") as f:
        for i in range(num_historical_weeks):
            params = {
                    "latest": latest,
                    "oldest": oldest, 
                    "limit": 1000,
                    }

            # API call
            r = requests.post("https://slack.com/api/conversations.history?channel={}&pretty=1".format(channel),
                              params = params,
                              headers = {"Authorization": "Bearer {}".format(auth_token)})

            # Check for errors
            if r.status_code != 200:
                print("ERROR: API returned Status {} due to {}".format(r.status_code, r.reason))
                exit()

            data  = r.json()["messages"]
            messages = [m for m in data if "has joined the channel" not in m["text"]]

            # Add to return file
            week_of_times.append(oldest)
            thread_counts.append(len(messages))

            # Write to file
            line = "{},{}\n".format(oldest, len(messages))
            f.write(line)

            print("{}: {}".format(oldest, len(messages)))

            # Advance the time barriers
            latest = oldest
            oldest = latest - seconds_in_a_week

    return week_of_times, thread_counts

# Plot Num Support Threads by Time
def plot(csvname):
    xs = []
    thread_counts = []

    with open(csvname, "r") as f:
        for line in f:
            vals = line.rstrip().split(",")
            unix_timestamp = float(vals[0])
            x = datetime.utcfromtimestamp(unix_timestamp).strftime("%m-%d")
            xs.append(x)
            thread_counts.append(int(vals[1]))

    plt.plot(xs, thread_counts, marker="o", markersize=8)
    plt.xlabel("Week", fontsize=20)
    plt.ylabel("Number of threads in channel", fontsize=20)
    plt.xticks(rotation = 90)
    plt.tick_params(axis='y', which='major', labelsize=10)
    plt.tick_params(axis='y', which='minor', labelsize=10)
    plt.tick_params(axis='x', which='major', labelsize=10)
    plt.tick_params(axis='x', which='minor', labelsize=10)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: python get-history.py <auth_token>")
        exit()
    auth_token = sys.argv[1]

    num_historical_weeks = 24
    channel = "CV3MTNZ6U"

    get_slack_history(auth_token, channel, num_historical_weeks)
    plot("./out.txt")

