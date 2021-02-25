import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style("darkgrid")

## REMINDER: REMOVE ADDITIONAL COMMAS IN WEBSITE DATA

def get_xs_ys(fpath, granularity):
    start = False
    xs = []
    ys = []
    xs_labels = []
    if "website" in fpath:
        x_index = 0
        for line in open(fpath):
            if start:
                try:
                    values = line.rstrip().replace("\"", "").split(",")
                    xs_labels.append(values[0])
                    view = int(values[1])
                    xs.append(x_index)
                    ys.append(view)
                    x_index += 1
                except:
                    pass
            if granularity in line:
                print("here!!!!")
                start = True
    if "analytics" in fpath:
        x_index = 0
        for line in open(fpath):
            if start:
                try:
                    values = line.rstrip().split(",")
                    xs_labels.append(values[0])
                    xs.append(x_index)
                    ys.append(int(values[1]))
                    x_index += 1
                except:
                    pass
            start = True
    return xs, ys, xs_labels

def plot_funnel(filepaths, labels, granularity):
    for fpath, label in zip(filepaths, labels):
        xs, ys, xs_labels = get_xs_ys(fpath, granularity)
        print(ys)
        plt.plot(xs, ys, marker="o", label=label)
        plt.legend()
        plt.xlabel(granularity)
        #plt.xticks(xs, xs_labels)
        plt.ylabel("Views")
    plt.ylim(ymin=0)
    plt.show()

def plot_conversion_rate(fpath1, fpath2, granularity, title):
    xs1, ys1, xs_labels1 = get_xs_ys(fpath1, granularity)
    xs2, ys2, xs_labels2 = get_xs_ys(fpath2, granularity)
    ys = [y2 * 100. / float(y1) for y1, y2 in zip(ys1, ys2)]
    print(ys)

    plt.plot(xs1, ys, marker="o")
    plt.xlabel(granularity)
    plt.ylabel("Conversion Rate")
    plt.ylim(ymin=0)
    plt.title(title)
    plt.show()





if  __name__ == "__main__":
    fpath1 = "data/2021-01-07/website_product_unique_9-1-1-6_month.csv"
    fpath2 = "data/2021-01-07/website_home_unique_9-1-1-6_month.csv"
    fpath3 = "data/2021-01-07/website_install-main_unique_9-1-1-6_month.csv"
    #fpath3 = "data/2021-01-07/website_install-main_9-1-1-6_month.csv"
    fpath4 = "data/2021-01-07/website_new-webui_9-1-1-6_month.csv"
    fpath5 = "data/2021-01-07/analytics_master-started_9-1-1-6_month.csv"

    #fpath4 = "data/2021-01-07/website_pytorch-mnist_9-1-1-6_month.csv"

    '''
    filepaths = [fpath1, fpath2, fpath3, fpath4, fpath5]
    labels = ["Product Page", "Website Home", "Install Home", "New Users to WebUI", "Masters Started"]
    plot_funnel(filepaths, labels, "Month")

    plot_conversion_rate(fpath3, fpath4, "Month", "Installation Followthrough (Install docs -> New WebUI users)")
    plot_conversion_rate(fpath2, fpath3, "Month", "Web home -> Install docs")
    '''

    fpath6 = "data/2021-01-07/website_new-webui_9-1-1-6_day.csv"
    fpath7  = "data/2021-01-07/analytics_master-started_9-1-1-6_day.csv"
    filepaths = [fpath3, fpath4]
    labels = ["Unique Visits to Install Docs", "New Users to WebUI"]
    plot_funnel(filepaths, labels, "Month")

