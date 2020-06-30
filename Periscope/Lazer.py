import pygame
import math
from MStat.Mirror import Mirror
from MStat.Cylinder import Cylinder

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Lazer:
    def __init__(self, screen, st_point, mir=Mirror(None), cyl=Cylinder(None)):
        if mir is None:
            mir = [0, 0]
        self.start = st_point
        self.d = [[-1, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.points = [st_point.copy(), [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.mir = mir
        self.sc = screen
        self.cyl = cyl

    def dot_cyl(self):
        vector = [self.cyl.bias[0] - self.points[len(self.mir)][0],
                  self.cyl.bias[1] - self.points[len(self.mir)][1],
                  self.cyl.bias[2] - self.points[len(self.mir)][2]]
        l = (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** 0.5
        for i in range(3):
            vector[i] /= l

        self.mir[len(self.mir) - 1].rot_vect(vector, -0.5)
        self.dot_point(len(self.mir) - 1, flag=False)
        t = -self.points[len(self.mir)][0] / self.d[len(self.mir)][0]
        point = [self.d[len(self.mir)][0] * t + self.points[len(self.mir)][0],
                 self.d[len(self.mir)][1] * t + self.points[len(self.mir)][1],
                 self.d[len(self.mir)][2] * t + self.points[len(self.mir)][2]]
        self.points[len(self.mir) + 1] = point

    def dot_point(self, index, flag=True):
        t = self.mir[index].find_point_plane(self.d[index], self.points[index])
        point = [self.d[index][0] * t + self.points[index][0],
                 self.d[index][1] * t + self.points[index][1],
                 self.d[index][2] * t + self.points[index][2]]
        if self.mir[index].dot_mirror(point):
            self.points[index + 1] = point
            self.d[index + 1] = self.mir[index].create_new_k(self.d[index])
            if flag:
                if index + 1 < len(self.mir):
                    self.dot(index=index + 1)
                else:
                    self.dot_cyl()

    def dot(self, index=0):
        if index != 0:
            vector = [self.mir[index].bias[0] - self.points[index][0],
                      self.mir[index].bias[1] - self.points[index][1],
                      self.mir[index].bias[2] - self.points[index][2]]
            l = (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** 0.5
            for i in range(3):
                vector[i] /= l
            self.mir[index-1].rot_vect(vector, 0.5)
            self.dot_point(index - 1, flag=False)
            self.mir[index].rot_vect(self.d[index], 1.0)
        self.dot_point(index)

    def draw(self, color=RED):
        for i in range(len(self.points) - 1):
            pygame.draw.line(self.sc, color, [self.points[i][0] + math.cos(math.pi / 4) * self.points[i][2],
                                              self.points[i][1] + math.cos(math.pi / 4) * self.points[i][2]],
                             [self.points[i + 1][0] + math.cos(math.pi / 4) * self.points[i + 1][2],
                              self.points[i + 1][1] + math.cos(math.pi / 4) * self.points[i + 1][2]], 1)

    def rebuild_lazer(self):
        centers, coef = self.cyl.getCentersAndCoef()
        vector = [self.cyl.bias[0] - self.points[len(self.mir)][0],
                  self.cyl.bias[1] - self.points[len(self.mir)][1],
                  self.cyl.bias[2] - self.points[len(self.mir)][2]]
        l = (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** 0.5
        for i in range(3):
            vector[i] /= l
        if abs(vector[0]) < coef[0] and abs(vector[1]) < coef[1] and abs(vector[0]) < coef[0]:
            self.mir[len(self.mir) - 1].rot_vect(vector, -0.5, vector2=self.d[len(self.mir)])
            self.dot_point(len(self.mir) - 1, flag=False)
            t = -self.points[len(self.mir)][0] / self.d[len(self.mir)][0]
            point = [self.d[len(self.mir)][0] * t + self.points[len(self.mir)][0],
                     self.d[len(self.mir)][1] * t + self.points[len(self.mir)][1],
                     self.d[len(self.mir)][2] * t + self.points[len(self.mir)][2]]
            self.points[len(self.mir) + 1] = point
        else:
            if vector[1] > 0.5 * coef[1]:
                self.cyl.bias[1] -= 5
            elif vector[1] < -0.5 * coef[1]:
                self.cyl.bias[1] += 5

            if vector[2] > 0.5 * coef[2]:
                self.cyl.bias[2] -= 5
            elif vector[2] < -0.5 * coef[2]:
                self.cyl.bias[2] += 5