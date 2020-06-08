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

    def seek_normal(self, vect1, vect2):
        x = vect1[1] * (vect2[2] - vect1[2]) - (vect2[1] - vect1[1]) * vect1
        y = -(vect1[0] * (vect2[2] - vect1[2]) -
              (vect2[0] - vect1[0]) * vect1[2])
        z = vect1[0] * (vect2[1] - vect1[1]) - \
            (vect2[0] - vect1[0]) * vect1[1]

    def vect_cent(self, vect1, vect2):
        return [(vect1[0] + vect2[0]) / 2, (vect1[1] + vect2[1]) / 2, (vect1[2] + vect2[2]) / 2]

    def delta_vec(self, vect1, vect2):
        return self.normal_vect([0, 0, 0], [vect2[0] - vect1[0], vect2[1] - vect1[1], vect2[2] - vect1[2]])

    def normal_vect(self, point1, point2):
        d = [point2[0] - point1[0],
             point2[1] - point1[1],
             point2[2] - point1[2]]
        normalize = (d[0] ** 2 + d[1] ** 2 + d[2] ** 2) ** 0.5
        d = [d[0] / normalize, d[1] / normalize, d[2] / normalize]
        print(normalize)
        return d

    def edit_rot(self, points, index):
        d = self.normal_vect(self.points[index + 1], points)
        rot1, rot2, rot3 = (math.acos(d[0]) - math.acos(self.d[index + 1][0])) / 2, \
                           (math.acos(d[1]) - math.acos(self.d[index + 1][1])) / 2, \
                           (math.acos(d[2]) - math.acos(self.d[index + 1][2])) / 2
        '''rotX = math.acos(d[0])
        rotY = math.acos(d[1]) + math.pi / 2
        rotZ = math.acos(d[2])
        self.mir[index].rot_set(rotX, rotY, rotZ, rebuild=False)'''
        self.mir[1].rot(rotY=-rot1, rotX=-rot2, rebuild=False)

    def process_cyl(self):
        points, k_max = self.cyl.getCentersAndCoef()
        d = self.normal_vect(self.points[2], points[0])
        coef_acc = 0.7
        length = points[0][0] - points[1][0]
        self.d[2] = self.mir[1].create_new_k(self.d[1])
        # k = abs(length / self.d[len(self.d) - 1][0])
        if abs(d[1]) < coef_acc * k_max[1] and abs(d[2]) < coef_acc * k_max[2]:
            while abs(self.d[2][1]) >= coef_acc * k_max[1]:
                sign = self.d[2][1] / abs(self.d[2][1])
                self.mir[1].rot(rotZ=sign * 0.05)
                self.d[2] = self.mir[1].create_new_k(self.d[1])

            while abs(self.d[2][2]) >= coef_acc * k_max[2]:
                sign = self.d[2][2] / abs(self.d[2][2])
                self.mir[1].rot(rotY=sign * 0.05)
                self.d[2] = self.mir[1].create_new_k(self.d[1])

            self.points[3] = [points[0][0] + self.d[len(self.d) - 1][0] * length,
                              points[0][1] + self.d[len(self.d) - 1][1] * length,
                              points[0][2] + self.d[len(self.d) - 1][2] * length]
        else:
            x = abs(points[0][0] - self.points[2][0])
            k = 0
            while abs(d[1]) < 2 * coef_acc * k_max[1] and abs(d[2]) < 2 * coef_acc * k_max[2]:
                d = self.normal_vect(self.points[2] + k * self.d[1], points[0])
            #self.mir[1].bias[0] += self.d[1][0] * x / length
            #self.mir[1].bias[1] += self.d[1][1] * x / length
            #self.mir[1].bias[2] += self.d[1][2] * x / length
            if abs(d[1]) >= coef_acc * k_max[1]:
                delta_y = self.d[2][1] * length
                self.mir[1].bias[1] += delta_y * x / length
            #delta_z = self.d[2][2] * length
            #self.mir[1].bias[2] += -delta_z * x / length

            self.points[2] = self.mir[1].bias.copy()
            #self.edit_rot(self.points[2], 0)
            self.d[2] = self.mir[1].create_new_k(self.d[1])
            self.mir[1].do_bias()
            self.points[3] = [points[0][0] + self.d[len(self.d) - 1][0] * length,
                              points[0][1] + self.d[len(self.d) - 1][1] * length,
                              points[0][2] + self.d[len(self.d) - 1][2] * length]
            self.process_cyl()
        '''coef_acc = 0.7
        points, k_max = self.cyl.getCentersAndCoef()
        length = points[0][0] - points[1][0]
        d = self.normal_vect(self.points[2], points[0])
        if abs(d[1]) < coef_acc * k_max[1] and abs(d[2]) < coef_acc * k_max[2]:
            self.edit_rot(points[0], 1)
            self.mir[1].dot_mirror(self.points[2], move=False)
            self.d[2] = self.mir[1].create_new_k(self.d[1])
            self.points[len(self.mir) + 1] = [points[0][0] + self.d[len(self.d) - 1][0] * length,
                                              points[0][1] + self.d[len(self.d) - 1][1] * length,
                                              points[0][2] + self.d[len(self.d) - 1][2] * length]
        else:
            x = abs(points[0][0] - self.points[2][0])


            self.dot(index=1)'''

    def dot(self, index=0):
        t = self.mir[index].find_point_plane(self.d[index], self.points[index])
        self.points[index + 1] = [self.d[index][0] * t + self.points[index][0],
                                  self.d[index][1] * t + self.points[index][1],
                                  self.d[index][2] * t + self.points[index][2]]
        '''if self.mir[index].dot_mirror(self.points[index + 1]):
            self.d.append(self.mir[index].create_new_k(self.d[index]))
            if index + 1 < len(self.mir):
                self.dot(index=index + 1)
            else:
                self.points.append([int(self.d[index + 1][0] * 100 + self.points[index + 1][0]),
                                    int(self.d[index + 1][1] * 100 + self.points[index + 1][1]),
                                    int(self.d[index + 1][2] * 100 + self.points[index + 1][2])])

            self.mir[index].set_rebuild_lazer(False)'''
        self.mir[index].dot_mirror(self.points[index + 1])
        self.d[index + 1] = self.mir[index].create_new_k(self.d[index])
        if index + 1 < len(self.mir):
            self.dot(index=index + 1)
        else:
            self.process_cyl()

        self.mir[index].set_rebuild_lazer(False)

    def delete(self, index=0):
        r = len(self.d)
        for i in range(r - 1, index, -1):
            self.d.remove(self.d[i])
        r = len(self.points)
        for i in range(r - 1, index, -1):
            self.points.remove(self.points[i])

    def draw(self, color=RED):
        for i in range(len(self.mir)):
            if self.mir[i].rebuildLazer:
                self.dot(index=i)
                for j in range(i, len(self.mir)):
                    self.mir[j].set_rebuild_lazer(False)
        for i in range(len(self.points) - 1):
            pygame.draw.line(self.sc, color, [self.points[i][0] + math.cos(math.pi / 4) * self.points[i][2],
                                              self.points[i][1] + math.cos(math.pi / 4) * self.points[i][2]],
                             [self.points[i + 1][0] + math.cos(math.pi / 4) * self.points[i + 1][2],
                              self.points[i + 1][1] + math.cos(math.pi / 4) * self.points[i + 1][2]], 1)
