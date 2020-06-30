import math
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Mirror:
    def __init__(self, screen, size=[640, 480], scale=1, bias=[0, 0, 0]):
        self.peaks = [[0, -1.2, 0.75], [0, 3.3, 0.75], [0, -1.2, -0.75]]
        self.sc = screen
        self.scale = scale
        self.bias = bias
        self.a_bias, self.b_bias, self.c_bias = [0, 0], [0, 0], [0, 0]
        self.do_bias()
        self.normal = [0., 0., 0.]
        self.do_normal()
        self.size = size

    def normalize(self):
        return (self.normal[0] ** 2 + self.normal[1] ** 2 + self.normal[2] ** 2) ** 0.5

    def do_normal(self):
        x = (self.peaks[1][1] - self.peaks[0][1]) * (self.peaks[2][2] - self.peaks[1][2]) - \
            (self.peaks[2][1] - self.peaks[1][1]) * (self.peaks[1][2] - self.peaks[0][2])
        y = -((self.peaks[1][0] - self.peaks[0][0]) * (self.peaks[2][2] - self.peaks[1][2]) -
              (self.peaks[2][0] - self.peaks[1][0]) * (self.peaks[1][2] - self.peaks[0][2]))
        z = (self.peaks[1][0] - self.peaks[0][0]) * (self.peaks[2][1] - self.peaks[1][1]) - \
            (self.peaks[2][0] - self.peaks[1][0]) * (self.peaks[1][1] - self.peaks[0][1])
        self.normal = [x, y, z]
        l = self.normalize()
        for i in range(3):
            self.normal[i] /= l

    def do_bias(self):
        self.a_bias = [self.bias[0] + (self.scale * self.peaks[0][0] +
                                       (self.scale * self.peaks[0][2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                       self.bias[1] + (self.scale * self.peaks[0][1] +
                                       (self.scale * self.peaks[0][2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]
        self.b_bias = [self.bias[0] + (self.scale * self.peaks[1][0] +
                                       (self.scale * self.peaks[1][2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                       self.bias[1] + (self.scale * self.peaks[1][1] +
                                       (self.scale * self.peaks[1][2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]
        self.c_bias = [self.bias[0] + (self.scale * self.peaks[2][0] +
                                       (self.scale * self.peaks[2][2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                       self.bias[1] + (self.scale * self.peaks[2][1] +
                                       (self.scale * self.peaks[2][2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]

    def draw(self, color=WHITE):
        pygame.draw.line(self.sc, color, [self.a_bias[0], self.a_bias[1]], [self.b_bias[0], self.b_bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.b_bias[0], self.b_bias[1]], [self.c_bias[0], self.c_bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.c_bias[0], self.c_bias[1]], [self.a_bias[0], self.a_bias[1]], 1)

    def rot(self, vector, alpha):
        for peak in self.peaks:
            temp = peak.copy()
            peak[0] = (math.cos(alpha) + (1 - math.cos(alpha)) * (vector[0] ** 2)) * temp[0] + \
                      ((1 - math.cos(alpha)) * vector[0] * vector[1] - math.sin(alpha) * vector[2]) * temp[1] + \
                      ((1 - math.cos(alpha)) * vector[0] * vector[2] + math.sin(alpha) * vector[1]) * temp[2]
            peak[1] = (math.cos(alpha) + (1 - math.cos(alpha)) * (vector[1] ** 2)) * temp[1] + \
                      ((1 - math.cos(alpha)) * vector[2] * vector[1] - math.sin(alpha) * vector[0]) * temp[2] + \
                      ((1 - math.cos(alpha)) * vector[0] * vector[1] + math.sin(alpha) * vector[2]) * temp[0]
            peak[2] = (math.cos(alpha) + (1 - math.cos(alpha)) * (vector[2] ** 2)) * temp[2] + \
                      ((1 - math.cos(alpha)) * vector[2] * vector[0] - math.sin(alpha) * vector[1]) * temp[0] + \
                      ((1 - math.cos(alpha)) * vector[2] * vector[1] + math.sin(alpha) * vector[0]) * temp[1]
        self.do_bias()

    def find_point_plane(self, k=[0, 0, 0], b=[0, 0, 0]):
        self.do_normal()
        return (self.normal[0] * (self.scale * self.peaks[0][0] + self.bias[0] - b[0]) +
                self.normal[1] * (self.scale * self.peaks[0][1] + self.bias[1] - b[1]) +
                self.normal[2] * (self.scale * self.peaks[0][2] + self.bias[2] - b[2])) / \
               (self.normal[0] * k[0] + self.normal[1] * k[1] + self.normal[2] * k[2])

    def dot_mirror(self, point, move=True):
        vP = [-self.scale * self.peaks[0][0] - self.bias[0] + point[0],
              -self.scale * self.peaks[0][1] - self.bias[1] + point[1],
              -self.scale * self.peaks[0][2] - self.bias[2] + point[2]]
        vAB = [self.scale * (self.peaks[1][0] - self.peaks[0][0]),
               self.scale * (self.peaks[1][1] - self.peaks[0][1]),
               self.scale * (self.peaks[1][2] - self.peaks[0][2])]
        vAC = [self.scale * (self.peaks[2][0] - self.peaks[0][0]),
               self.scale * (self.peaks[2][1] - self.peaks[0][1]),
               self.scale * (self.peaks[2][2] - self.peaks[0][2])]

        det_v = (vAB[2] * vAC[1] - vAB[1] * vAC[2])
        if det_v != 0:
            k = (vP[2] * vAC[1] - vP[1] * vAC[2]) / det_v
            f = (vAB[2] * vP[1] - vAB[1] * vP[2]) / det_v
            if 0 <= k <= 1 and 0 <= f <= 1 and k + f <= 1 and move:
                return True
            else:
                return False
        else:
            return False

    def create_new_k(self, d=[0, 0, 0]):
        self.do_normal()
        len1 = (self.normal[0] ** 2 + self.normal[1] ** 2 + self.normal[2] ** 2) ** 0.5
        v = [-self.normal[0] / len1, -self.normal[1] / len1, -self.normal[2] / len1]
        sc = v[0] * d[0] + v[1] * d[1] + v[2] * d[2]
        k = [0, 0, 0]
        eps = 1e-10
        k[0] = d[0] - 2 * v[0] * sc + eps
        k[1] = d[1] - 2 * v[1] * sc + eps
        k[2] = d[2] - 2 * v[2] * sc + eps
        return k

    def rot_vect(self, vector1, coef, vector2=None):
        self.do_normal()
        if vector2 is None:
            vectRotate = [vector1[1] * self.normal[2] - vector1[2] * self.normal[1],
                          -(vector1[0] * self.normal[2] - vector1[2] * self.normal[0]),
                          vector1[0] * self.normal[1] - vector1[1] * self.normal[0]]
            l = (vectRotate[0] ** 2 + vectRotate[1] ** 2 + vectRotate[2] ** 2) ** 0.5
            for i in range(3):
                vectRotate[i] /= l

            l = (vector1[0] ** 2 + vector1[1] ** 2 + vector1[2] ** 2) ** 0.5
            for i in range(3):
                vector1[i] /= l

            alpha = math.acos(vector1[0] * self.normal[0] + vector1[1] * self.normal[1] + vector1[2] * self.normal[2])
        else:
            vectRotate = [vector1[1] * vector2[2] - vector1[2] * vector2[1],
                          -(vector1[0] * vector2[2] - vector1[2] * vector2[0]),
                          vector1[0] * vector2[1] - vector1[1] * vector2[0]]
            l = (vectRotate[0] ** 2 + vectRotate[1] ** 2 + vectRotate[2] ** 2) ** 0.5
            for i in range(3):
                vectRotate[i] /= l

            l = (vector1[0] ** 2 + vector1[1] ** 2 + vector1[2] ** 2) ** 0.5
            for i in range(3):
                vector1[i] /= l

            l = (vector2[0] ** 2 + vector2[1] ** 2 + vector2[2] ** 2) ** 0.5
            for i in range(3):
                vector2[i] /= l

            alpha = math.acos(vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2])

        self.rot(vectRotate, coef * alpha)