import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

count_elem = [20, 100]
distribution = ['Normal', 'Cauchy', 'Laplace', 'Poisson', 'Uniform']
N = 1000


def get_array(name, n):
    if name == distribution[0]:
        return np.random.normal(0, 1, n)
    elif name == distribution[1]:
        return np.random.standard_cauchy(n)
    elif name == distribution[2]:
        return np.random.laplace(0, np.sqrt(2) / 2, n)
    elif name == distribution[3]:
        return np.random.poisson(10, n)
    else:
        return np.random.uniform(-np.sqrt(3), np.sqrt(3), n)


def lab3_run():
    title_row = ["Distribution", "Proportion of emissions"]
    rows = []
    for dist_str in distribution:
        arr_20, arr_100 = get_array(dist_str, count_elem[0]), get_array(dist_str, count_elem[1])
        plt.boxplot((arr_20, arr_100), whiskerprops=dict(color="black", linestyle="dashdot"), boxprops=dict(color="b"),
                    flierprops=dict(marker="o", markersize=4), labels=["n = 20", "n = 100"])
        plt.ylabel("X")
        plt.title(dist_str)
        plt.show()
        #plt.savefig(dist_str + '.png', format='png')

        count = [0, 0]

        for i in range(N):
            arr_emis_20, arr_emis_100 = get_array(dist_str, count_elem[0]), get_array(dist_str, count_elem[1])

            emis_20, emis_100 = [], []

            emis_20.append(2.5 * np.quantile(arr_emis_20, 0.25) - 1.5 * np.quantile(arr_emis_20, 0.75))
            emis_20.append(2.5 * np.quantile(arr_emis_20, 0.75) - 1.5 * np.quantile(arr_emis_20, 0.25))

            emis_100.append(2.5 * np.quantile(arr_emis_100, 0.25) - 1.5 * np.quantile(arr_emis_100, 0.75))
            emis_100.append(2.5 * np.quantile(arr_emis_100, 0.75) - 1.5 * np.quantile(arr_emis_100, 0.25))

            for k in range(count_elem[0]):
                if emis_20[1] < arr_emis_20[k] or arr_emis_20[k] < emis_20[0]:
                    count[0] += 1

            for k in range(count_elem[1]):
                if emis_100[1] < arr_emis_100[k] or arr_emis_100[k] < emis_100[0]:
                    count[1] += 1

        count[0] /= (20 * N)
        count[1] /= (100 * N)

        rows.append([dist_str + ", n = 20", np.around(count[0], decimals=2)])
        rows.append([2 * ""])
        rows.append([dist_str + ", n = 100", np.around(count[1], decimals=2)])
        rows.append([2 * ""])

    print(tabulate(rows, title_row, tablefmt="latex"), end="\n\n")
