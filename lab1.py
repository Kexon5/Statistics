import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial

count_elem = [10, 50, 1000]
distribution = ['Normal', 'Cauchy', 'Laplace', 'Poisson', 'Uniform']
count_bins = 20


def normal(N):
    mu, sigma = 0, 1
    s = np.random.normal(mu, sigma, N)
    n, bins, patches = plt.hist(s, count_bins, density=1, facecolor='green', edgecolor='black', alpha=0.3)
    plt.plot(bins, 1 / (np.sqrt(2 * np.pi)) * np.exp(- bins ** 2 / 2), color='b', linewidth=1)


def cauchy(N):
    s = np.random.standard_cauchy(N)
    n, bins, patches = plt.hist(s, count_bins, density=1, facecolor='green', edgecolor='black', alpha=0.3)
    plt.plot(bins, 1 / (np.pi * (bins * bins + 1)), color='b', linewidth=1)


def laplace(N):
    mu, sigma = 0, np.sqrt(2)
    s = np.random.laplace(mu, sigma, N)
    n, bins, patches = plt.hist(s, count_bins, density=1, facecolor='green', edgecolor='black', alpha=0.3)
    plt.plot(bins, 1 / np.sqrt(2) * np.exp(-np.sqrt(2) * np.fabs(bins)), color='b', linewidth=1)


def poisson(N):
    s = np.random.poisson(10, N)
    n, bins, patches = plt.hist(s, count_bins, density=1, facecolor='green', edgecolor='black', alpha=0.3)
    plt.plot(bins, np.power(10, bins) * np.exp(-10) / factorial(bins), color='b', linewidth=1)


def uniform(N):
    s = np.random.uniform(-np.sqrt(3), np.sqrt(3), N)
    n, bins, patches = plt.hist(s, count_bins, density=1, facecolor='green', edgecolor='black', alpha=0.3)
    help = []
    ar = np.arange(-2., 2., 0.01)
    for elem in ar:
        if np.fabs(elem) <= np.sqrt(3):
            help.append(1 / (2 * np.sqrt(3)))
        else:
            help.append(0)
    plt.plot(ar, help, color='b', linewidth=1)


def switch_disribution(name, N):
    if name == distribution[0]:
        normal(N)
    elif name == distribution[1]:
        cauchy(N)
    elif name == distribution[2]:
        laplace(N)
    elif name == distribution[3]:
        poisson(N)
    else:
        uniform(N)


def lab1_run():
    for dist_str in distribution:
        index_graph = 1
        plt.suptitle(dist_str + " Distribution")
        for N in count_elem:
            plt.subplot(1, 3, index_graph)
            index_graph += 1
            switch_disribution(dist_str, N)
            plt.title(dist_str + ' Distribution, N=%i' % N)
            plt.xlabel(dist_str + ' Numbers')
            plt.ylabel('Density')
            plt.subplots_adjust(wspace=0.5)
        #plt.savefig(dist_str + '.png', format='png')
        plt.show()
