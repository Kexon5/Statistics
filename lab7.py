import numpy as np
import scipy.stats as stats
from tabulate import tabulate

N = 10


def lab7_run():
    dist = np.random.normal(0, 1, N)

    mu = np.mean(dist)
    sigma = np.std(dist)
    print('Выборочное среднее mu = ', mu)
    print('Выборочная дисперсия sigma = ', sigma)

    alpha = 0.05
    not_alpha = 1 - 0.05
    k = 6

    subset = np.linspace(-2, 2, k - 1)

    probability = [stats.norm.cdf(subset[0])]
    count_el = [len(dist[dist <= subset[0]])]

    for i in range(len(subset) - 1):
        probability += [stats.norm.cdf(subset[i + 1]) - stats.norm.cdf(subset[i])]
        count_el += [len(dist[(dist <= subset[i + 1]) & (dist >= subset[i])])]

    probability += [1 - stats.norm.cdf(subset[-1])]
    count_el += [len(dist[dist >= subset[-1]])]

    probability = np.array(probability)
    count_el = np.array(count_el)
    res = np.divide(np.multiply((count_el - N * probability), (count_el - N * probability)), N * probability)

    rows = []
    headers = ["i", "limits", "n_i", "p_i", "np_i", "n_i - np_i", "(n_i - np_i)^2 / (np_i)"]

    for i in range(len(count_el)):
        if i == 0:
            interval = ['-inf', subset[0]]
        elif i == len(count_el) - 1:
            interval = [subset[-1], 'inf']
        else:
            interval = [subset[i - 1], subset[i]]
        rows.append(
            [i + 1, interval, count_el[i], np.around(probability[i], decimals=4), np.around(probability[i] * N, decimals=2),
             np.around(count_el[i] - N * probability[i], decimals=2), np.around(res[i], decimals=2)])
    rows.append(['itog', "-", np.sum(count_el), np.around(np.sum(probability), decimals=4),
                 np.around(np.sum(N * probability), decimals=2),
                 -np.around(np.sum(count_el - N * probability), decimals=2),
                 np.around(np.sum(res), decimals=2)])
    print(tabulate(rows, headers, tablefmt="latex"))
    print('\n')
