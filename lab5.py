import numpy as np
import scipy.stats as stats
from tabulate import tabulate
import matplotlib.pyplot as plt
import math

count_elem = [20, 60, 100]
cor_сoef = [0, 0.5, 0.9]
N = 1000


def make_table(p_coef, s_coef, q_coef, size, rho, strs):
    rows = []
    p = [np.mean(p_coef), np.mean([p_coef[i] ** 2 for i in range(N)]), np.var(p_coef)]
    s = [np.mean(s_coef), np.mean([s_coef[i] ** 2 for i in range(N)]), np.var(s_coef)]
    q = [np.mean(q_coef), np.mean([q_coef[i] ** 2 for i in range(N)]), np.var(q_coef)]
    row_value = ['E(z)', 'E(z^{2})', 'D(z)']
    rows.append([strs, 'r', 'r_{S}', 'r_{Q}'])
    for i in range(len(p)):
        rows.append([row_value[i], np.around(p[i], decimals=3),
                     np.around(s[i], decimals=3),np.around(q[i], decimals=3)])
    print(tabulate(rows, [],  tablefmt="latex"))
    print('\n')


def quadrant(x, y):
    med_x, med_y = np.median(x), np.median(y)
    size = len(x)
    x_new, y_new = [x[i] - med_x for i in range(size)], [y[i] - med_y for i in range(size)]
    n = [0, 0, 0, 0]
    for i in range(size):
        if x_new[i] >= 0 and y_new[i] >= 0:
            n[0] += 1
        if x_new[i] < 0 and y_new[i] > 0:
            n[1] += 1
        if x_new[i] < 0 and y_new[i] < 0:
            n[2] += 1
        if x_new[i] > 0 and y_new[i] < 0:
            n[3] += 1
    return ((n[0] + n[2]) - (n[1] + n[3])) / size


def fun_normal(count, rho):
    return stats.multivariate_normal.rvs(cov=[[1.0, rho], [rho, 1.0]], size=count)


def fun_mix(count):
    drv = []
    for j in range(2):
        drv += list(0.9 * stats.multivariate_normal.rvs(cov=[[1, 0.9], [0.9, 1]], size=count)
                + 0.1 * stats.multivariate_normal.rvs(cov=[[10, -0.9], [-0.9, 10]], size=count))

    return np.array(drv)


def seek_coef(count, rho):
    pearson_coef, spearman_coef, quadrant_coef = [np.empty(N), np.empty(N), np.empty(N)]
    for i in range(N):
        if rho != -1:
            drv = fun_normal(count, rho)
        else:
            drv = fun_mix(count)
        x, y = drv[:, 0], drv[:, 1]
        pearson_coef[i] = stats.pearsonr(x, y)[0]
        spearman_coef[i] = stats.spearmanr(x, y)[0]
        quadrant_coef[i] = quadrant(x, y)
    return pearson_coef, spearman_coef, quadrant_coef


def normal_distribution(count):
    for rho in cor_сoef:
        pearson_coef, spearman_coef, quadrant_coef = seek_coef(count, rho)
        make_table(pearson_coef, spearman_coef, quadrant_coef, count, rho, 'rho = ' + str(rho))


def mix_normal_distribution(count):
    pearson_coef, spearman_coef, quadrant_coef = seek_coef(count, -1)
    make_table(pearson_coef, spearman_coef, quadrant_coef, count, -1, 'n = ' + str(count))


def ellipse(x,y):
    cov_coef = stats.pearsonr(x, y)[0]

    center_x = np.mean(x)
    center_y = np.mean(y)

    a = 3 * np.sqrt(np.cov(x,y)[0, 0] * (1 + cov_coef))
    b = 3 * np.sqrt(np.cov(x,y)[1, 1] * (1 - cov_coef))

    t_rot = math.pi / 4

    t = np.linspace(0, 2 * math.pi, 100)
    ell = np.array([a * np.cos(t), b * np.sin(t)])
    matr_rot = np.array([[math.cos(t_rot), -math.sin(t_rot)], [math.sin(t_rot), math.cos(t_rot)]])

    ell_rot = np.zeros((2, ell.shape[1]))
    for i in range(ell.shape[1]):
        ell_rot[:, i] = np.dot(matr_rot, ell[:, i])

    plt.plot(center_x + ell_rot[0, :], center_y + ell_rot[1, :], c='black')


def my_plot(count):
    plt.suptitle("n = " + str(count))
    titles = [r'$ \rho = 0$', r'$\rho = 0.5 $', r'$ \rho = 0.9$']
    num = 0
    index_graph = 1
    for rho in cor_сoef:
        plt.subplot(1, 3, index_graph)
        rv = stats.multivariate_normal.rvs(cov=[[1.0, rho], [rho, 1.0]], size=count)
        x = rv[:, 0]
        y = rv[:, 1]
        plt.scatter(x, y, s=2)
        ellipse(x, y)
        plt.scatter(np.mean(x), np.mean(y), color='red', s=2)
        plt.title(titles[index_graph - 1])
        num += 1
        index_graph += 1
    #plt.savefig(str(count) + ".png", format='png')
    plt.show()


def lab5_run():
    for count in count_elem:
        normal_distribution(count)
        mix_normal_distribution(count)
        my_plot(count)
