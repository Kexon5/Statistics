import numpy as np
from tabulate import tabulate

count_elem = [10, 100, 1000]
distribution = ['Normal', 'Cauchy', 'Laplace', 'Poisson', 'Uniform']
N = 1000


def fun_z_q(arr):
    return (np.quantile(arr, 0.25) + np.quantile(arr, 0.75)) / 2


def fun_z_tr(arr):
    r = len(arr) // 4
    arr_new = np.sort(arr)
    sum = 0
    for i in range(r + 1, len(arr) - r):
        sum += arr_new[i]
    return sum / (len(arr) - 2 * r)


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


def lab2_run():
    for dist_str in distribution:
        title_row = [dist_str, "x_", "med x", "z_r", "z_q", "z_tr"]
        rows = []
        for n in count_elem:
            x, med, z_r, z_q, z_tr = [], [], [], [], []
            for i in range(N):
                arr = get_array(dist_str, n)

                x.append(np.mean(arr))

                med.append(np.median(arr))

                arr_sort = np.sort(arr)
                z_r.append((arr_sort[0] + arr_sort[-1]) / 2)

                z_q.append(fun_z_q(arr))

                z_tr.append(fun_z_tr(arr))
            rows.append(["n = %i" % n, 6 * ""])
            rows.append([" E(z) ",
                         np.around(np.mean(x), decimals=6),
                         np.around(np.mean(med), decimals=6),
                         np.around(np.mean(z_r), decimals=6),
                         np.around(np.mean(z_q), decimals=6),
                         np.around(np.mean(z_tr), decimals=6)])
            rows.append([" D(z) ",
                         np.around(np.std(x) ** 2, decimals=6),
                         np.around(np.std(med) ** 2, decimals=6),
                         np.around(np.std(z_r) ** 2, decimals=6),
                         np.around(np.std(z_q) ** 2, decimals=6),
                         np.around(np.std(z_tr) ** 2, decimals=6)])
            rows.append(["" * 7])
        print(tabulate(rows, title_row, tablefmt="latex"), end="\n\n")
