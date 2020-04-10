import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.distributions.empirical_distribution import ECDF
import seaborn as sns

count_elem = [20, 60, 100]
distribution = ['Normal', 'Cauchy', 'Laplace', 'Poisson', 'Uniform']


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


def get_distribution_func(dist_str, arr):
    if dist_str == distribution[0]:
        return stats.norm.cdf(arr)
    elif dist_str == distribution[1]:
        return stats.cauchy.cdf(arr)
    elif dist_str == distribution[2]:
        return stats.laplace.cdf(arr)
    elif dist_str == distribution[3]:
        return stats.poisson.cdf(arr, 10)
    else:
        return stats.uniform.cdf(arr)


def get_distribution_density(dist_str, arr):
    if dist_str == distribution[0]:
        return stats.norm.pdf(arr, 0, 1)
    elif dist_str == distribution[1]:
        return stats.cauchy.pdf(arr)
    elif dist_str == distribution[2]:
        return stats.laplace.pdf(arr, 0, 1 / 2 ** 0.5)
    elif dist_str == distribution[3]:
        return stats.poisson.pmf(10, arr)
    else:
        return stats.uniform.pdf(arr, -3 ** 0.5, 2 * 3 ** 0.5)


def lab4_run():
    for dist_str in distribution:
        if dist_str == distribution[3]:
            arr_common = np.arange(6, 14, 0.01)
            arr_cropped = [list(filter(lambda x: x if 6 <= x <= 14 else [],
                                       get_array(dist_str, count_elem[j]))) for j in range(len(count_elem))]
        else:
            arr_common = np.arange(-4, 4, 0.01)
            arr_cropped = [list(filter(lambda x: x if -4 <= x <= 4 else [],
                                       get_array(dist_str, count_elem[j]))) for j in range(len(count_elem))]

        index_graph = 1
        for arr in arr_cropped:
            plt.subplot(1, 3, index_graph)
            plt.title(dist_str + ', n = ' + str(count_elem[index_graph - 1]))
            plt.plot(arr_common, get_distribution_func(dist_str, arr_common), color='blue', linewidth=0.8)
            ecdf = ECDF(arr)
            y = ecdf(arr_common)
            plt.step(arr_common, y, color='black')
            plt.xlabel('x')
            plt.ylabel('F(x)')
            plt.subplots_adjust(wspace=0.5)
            index_graph += 1
        plt.show()

        j = 1
        for arr in arr_cropped:

            titles = [r'$h = \frac{h_n}{2}$', r'$h = h_n$', r'$h = 2 * h_n$']
            index_graph = 1
            plt.suptitle(dist_str + ', n = ' + str(count_elem[j - 1]))
            j += 1

            for bandwidth in [0.5, 1, 2]:
                plt.subplot(1, 3, index_graph)
                kde = stats.gaussian_kde(arr, bw_method='silverman')
                plt.plot(arr_common, get_distribution_density(dist_str, arr_common), color='blue',
                         label='density')
                sns.kdeplot(arr, bw=kde.factor * bandwidth, label='kde')

                plt.title(titles[index_graph - 1])
                plt.xlabel('x')
                plt.ylabel('F(x)')
                plt.subplots_adjust(wspace=0.5)
                plt.ylim([0, 1])
                if dist_str == distribution[3]:
                    plt.xlim([6, 14])
                else:
                    plt.xlim([-4, 4])

                plt.legend()
                index_graph += 1

            plt.show()
