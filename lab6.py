import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

def mnk(x, y):
    b1 = (np.mean(x * y) - np.mean(x) * np.mean(y)) / (np.mean(x * x) - np.mean(x) ** 2)
    b0 = np.mean(y) - b1 * np.mean(x)
    return b0, b1


def f_min(param, x,y):
    '''a0, a1 = param
    return sum(abs(y - (a0 * x + a1)))'''
    a_1, a_2 = param
    res = 0
    for i in range(len(x)):
        res += abs(a_1 * x[i] + a_2 - y[i])
    return res


def my_plot(x, y, titles):
    b0, b1 = mnk(x, y)

    print('МНК')
    print('b0 = ', b0)
    print('b1 = ', b1)

    coef = opt.minimize(f_min, [b0, b1], args=(x, y)).x
    a0, a1 = coef[0], coef[1]

    print('МНМ')
    print('a0 = ', a0)
    print('a1 = ', a1)

    plt.scatter(x, y, label='Выборка', edgecolor='navy')
    plt.plot(x, x * (2 * np.ones(len(x))) + 2 * np.ones(len(x)), label='Модель', color='red')
    plt.plot(x, x * (b1 * np.ones(len(x))) + b0 * np.ones(len(x)), label='МHK', color='blue')
    plt.plot(x, x * (a1 * np.ones(len(x))) + a0 * np.ones(len(x)), label='МHM', color='green')

    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim([-1.9, 2.1])
    plt.legend()
    plt.title(titles)
    plt.savefig(titles + '.png', format='png')
    plt.show()


def lab6_run():
    x = np.arange(-1.8, 2, 0.2)
    y = 2 * np.ones(len(x)) + 2 * x + np.random.normal(0, 1, size=len(x))
    my_plot(x,y, 'Без возмущений')
    y[0] += 10
    y[-1] -= 10
    my_plot(x, y, 'С возмущениями')

