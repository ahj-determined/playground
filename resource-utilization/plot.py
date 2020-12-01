import ast
import json
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
from dateutil import parser, tz
import seaborn as sns
sns.set_theme(style="white")

utc_tz = tz.gettz('UTC')

def plot_stacked_bar(xs, ys_by_stack, xlabel, ylabel):
    index = pd.Index(xs, name='test')
    df = pd.DataFrame(ys_by_stack, index=index)
    #ax = df.plot(kind='bar', stacked=True, figsize=(10, 6))
    ax = df.plot(kind='bar', stacked=True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.legend(bbox_to_anchor=(1.0, 1), loc='upper left')
    plt.tight_layout()
    # plt.savefig('stacked.png')  # if needed
    plt.show()

def plot_bar(xs, ys, xlabel, ylabel):
    plt.bar(xs, ys)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def process_labels(labels):
    if labels == "":
        labels = [None]
    else:
        arr_str = json.loads(labels)
        arr_str = arr_str[1:-1]
        labels = arr_str.split(',')
    return(labels)

def run(csv):
    days = []
    minutes = []
    header = True

    time_by_month = defaultdict(int)
    time_by_day = defaultdict(int)

    time_by_month_by_user = defaultdict(lambda: defaultdict(int))
    time_by_day_by_user = defaultdict(lambda: defaultdict(int))

    time_by_month_by_label = defaultdict(lambda: defaultdict(int))
    time_by_day_by_label = defaultdict(lambda: defaultdict(int))

    # First run through dataset to get top users, labels
    time_by_user = defaultdict(int)
    time_by_label = defaultdict(int)
    days = set()
    months = set()
    header = True
    with open(csv) as f:
        for line in f:
            if header:
                header = False
                continue
            vals = line.rstrip().replace("\"\"", "").split("|")
            user = vals[1]
            labels = vals[3]
            labels = process_labels(labels)
            agent_types = vals[2]
            start_time = vals[5]
            time_elapsed = float(vals[6]) / 3600.

            time_by_user[user] += time_elapsed
            for label in labels:
                time_by_label[label] += time_elapsed

            day = start_time.split(" ")[0]
            elems = day.split("-")
            month = elems[0] + "-" + elems[1]
            days.add(day)
            months.add(month)

    ranked_items = list(reversed(sorted(time_by_user.items(), key=lambda item: item[1])))
    ranked_users = [i[0] for i in ranked_items]
    
    ranked_items = list(reversed(sorted(time_by_label.items(), key=lambda item: item[1])))
    ranked_labels= [i[0] for i in ranked_items]

    top_users = ranked_users[:4]
    top_labels = ranked_labels[:4]

    for user in top_users + ["Other"]:
        for day in days:
            time_by_day_by_user[user][day] = 0.0
        for month in months:
            time_by_month_by_user[user][month] = 0.0

    for label in top_labels + ["Other"]:
        for day in days:
            time_by_day_by_label[label][day] = 0.0
        for month in months:
            time_by_month_by_label[label][month] = 0.0

    header = True
    with open(csv) as f:
        for line in f:
            if header:
                header = False
                continue
            vals = line.rstrip().replace("\"\"", "").split("|")
            eid = int(vals[0])
            user = vals[1]
            agent_ids = vals[2]
            labels = process_labels(vals[3])
            slots = int(vals[4])
            start_time = vals[5]
            time_elapsed = float(vals[6]) / 3600.

            day = start_time.split(" ")[0]
            elems = day.split("-")
            month = elems[0] + "-" + elems[1]

            time_by_month[month] += time_elapsed * slots
            time_by_day[day] += time_elapsed * slots

            if user in top_users:
                time_by_month_by_user[user][month] += time_elapsed * slots
                time_by_day_by_user[user][day] += time_elapsed * slots
            else:
                time_by_month_by_user["Other"][month] += time_elapsed * slots
                time_by_day_by_user["Other"][day] += time_elapsed * slots

            for label in labels:
                if label in top_labels:
                    time_by_month_by_label[label][month] += time_elapsed * slots
                    time_by_day_by_label[label][day] += time_elapsed * slots
                else:
                    time_by_month_by_label["Other"][month] += time_elapsed * slots
                    time_by_day_by_label["Other"][day] += time_elapsed * slots

    # Utilization by Month

    months = sorted(time_by_month.keys())
    months_ys = [time_by_month[month] for month in months]
    plot_bar(months, months_ys, "Month", "GPU hours")

    # Utilization by Month

    days = sorted(time_by_day.keys())
    days_ys = [time_by_day[day] for day in days]
    plot_bar(days, days_ys, "Day", "GPU hours")

    # Utilization by Month by User
    ys_by_stack = {}
    for user, d_time_by_month in time_by_month_by_user.items():
        keys = sorted(d_time_by_month.keys())
        ys = []
        for k in keys:
            ys.append(d_time_by_month[k])
        ys_by_stack[user] = ys
    plot_stacked_bar(months, ys_by_stack, "Month", "GPU hours")

    # Utilization by Day by User
    '''
    time_by_month_by_user = {angela: {01/02: 200, 01/03: 100}
                             determined: {01/02: 100, 01/03: 150}
                             Other: {01/02: 0, 01/03: 40}}

    ys = {angela: [200, 100], determined: [100, 150], other: [0, 300]}
    '''
    ys_by_stack = {}
    for user, d_time_by_day in time_by_day_by_user.items():
        keys = sorted(d_time_by_day.keys())
        ys = []
        for k in keys:
            ys.append(d_time_by_day[k])
        ys_by_stack[user] = ys
    plot_stacked_bar(days, ys_by_stack, "Day", "GPU hours")

    # Utilization by Month by Label
    ys_by_stack = {}
    for label, d_time_by_month in time_by_month_by_label.items():
        keys = sorted(d_time_by_month.keys())
        ys = []
        for k in keys:
            ys.append(d_time_by_month[k])
        ys_by_stack[label] = ys
    plot_stacked_bar(months, ys_by_stack, "Month", "GPU hours")

    # Utilization by Day by Label
    ys_by_stack = {}
    for label, d_time_by_day in time_by_day_by_label.items():
        keys = sorted(d_time_by_day.keys())
        ys = []
        for k in keys:
            ys.append(d_time_by_day[k])
        ys_by_stack[label] = ys
    plot_stacked_bar(days, ys_by_stack, "Day", "GPU hours")

if __name__ == "__main__":
    run("./full.csv")
