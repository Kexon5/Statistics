import numpy as np
from tabulate import tabulate
import scipy.stats as stats

gamma = 0.95
count_elem = [20, 100]


def m_interval(dist, size):
    m = np.mean(dist)
    s = np.std(dist)
    interval = s * stats.t.ppf((1 + gamma) / 2, size - 1) / (size - 1) ** 0.5
    return m - interval, m + interval


def varience_interval(dist, size):
    s = np.std(dist)
    left = s * (size / stats.chi2.ppf((1 + gamma) / 2, size - 1)) ** 0.5
    right = s * (size / stats.chi2.ppf((1 - gamma) / 2, size - 1)) ** 0.5
    return left, right


def m_interval_as(dist, size):
    m = np.mean(dist)
    s = np.std(dist)
    u = stats.norm.ppf((1 + gamma) / 2)
    interval = s * u / (size ** 0.5)
    return m - interval, m + interval


def varience_interval_as(dist, size):
    m = np.mean(dist)
    s = np.std(dist)
    m_4 = stats.moment(dist, 4)
    e = m_4 / s ** 4 - 3
    u = stats.norm.ppf((1 + gamma) / 2)
    U = u * (((e + 2) / size) ** 0.5)
    left = s * (1 + 0.5 * U) ** (-0.5)
    right = s * (1 - 0.5 * U) ** (-0.5)
    return left, right


def lab8_run():
    rows = []
    for size in count_elem:
        dist = np.random.normal(0, 1, size)
        rows.append(['n = ' + str(size), 'm', 'sigma'])
        interval_m = np.around(m_interval_as(dist, size), decimals=2)
        '''m_interval_as(dist, size)'''
        interval_var = np.around(varience_interval_as(dist, size), decimals=2)
        '''varience_interval_as(dist, size)'''
        rows.append(["", str(interval_m[0]) + ' < m < ' + str(interval_m[1]),
                    str(interval_var[0]) + ' < sigma < ' + str(interval_var[1])])
        rows.append(3 * [])

    print(tabulate(rows, [], tablefmt="latex"))
    print('\n')

