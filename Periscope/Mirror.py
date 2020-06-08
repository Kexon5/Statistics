import math
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Mirror:
    def __init__(self, screen, size=[640, 480], scale=1, bias=[0, 0, 0]):
        self.peaks = [[0.7, 0, 0.5], [-1.8, 0, 0.5], [0, 0, -0.8]]
        self.peaksC = self.peaks.copy()
        self.sc = screen
        self.scale = scale
        self.bias = bias
        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
        self.a_bias, self.b_bias, self.c_bias = [0, 0], [0, 0], [0, 0]
        self.do_bias()
        self.normal = [0., 0., 0.]
        self.do_normal()
        self.rebuildLazer = False
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

    def do_bias(self):
        self.a_bias = [self.bias[0] + (self.scale * self.peaks[0][0] +
                                       (self.scale * self.peaks[0][2] + self.bias[2]) * math.cos(math.pi / 4)),
                       self.bias[1] + (self.scale * self.peaks[0][1] +
                                       (self.scale * self.peaks[0][2] + self.bias[2]) * math.cos(math.pi / 4))]
        self.b_bias = [self.bias[0] + (self.scale * self.peaks[1][0] +
                                       (self.scale * self.peaks[1][2] + self.bias[2]) * math.cos(math.pi / 4)),
                       self.bias[1] + (self.scale * self.peaks[1][1] +
                                       (self.scale * self.peaks[1][2] + self.bias[2]) * math.cos(math.pi / 4))]
        self.c_bias = [self.bias[0] + (self.scale * self.peaks[2][0] +
                                       (self.scale * self.peaks[2][2] + self.bias[2]) * math.cos(math.pi / 4)),
                       self.bias[1] + (self.scale * self.peaks[2][1] +
                                       (self.scale * self.peaks[2][2] + self.bias[2]) * math.cos(math.pi / 4))]

    def draw(self, color=WHITE):

        pygame.draw.line(self.sc, color, [self.a_bias[0], self.a_bias[1]], [self.b_bias[0], self.b_bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.b_bias[0], self.b_bias[1]], [self.c_bias[0], self.c_bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.c_bias[0], self.c_bias[1]], [self.a_bias[0], self.a_bias[1]], 1)

    def rot(self, rotX=0.0, rotY=0.0, rotZ=0.0, rebuild=True):
        if rotZ != 0.0:
            self.rotZ += rotZ
            if self.rotZ > 2 * math.pi:
                self.rotZ -= 2 * math.pi
            for peak in self.peaks:
                temp = peak.copy()
                peak[0] = math.cos(rotZ) * temp[0] + temp[1] * math.sin(rotZ)
                peak[1] = temp[1] * math.cos(rotZ) - temp[0] * math.sin(rotZ)

        if rotY != 0.0:
            self.rotY += rotY
            if self.rotY > 2 * math.pi:
                self.rotY -= 2 * math.pi
            for peak in self.peaks:
                temp = peak.copy()
                peak[2] = math.cos(rotY) * temp[2] + 0.5 * temp[0] * math.sin(rotY)
                peak[0] = temp[0] * math.cos(rotY) - 2 * temp[2] * math.sin(rotY)

        if rotX != 0.0:
            self.rotX += rotX
            if self.rotX > 2 * math.pi:
                self.rotX -= 2 * math.pi
            if abs(self.rotX - math.pi / 2) > 1e-1 and abs(self.rotX - 3 * math.pi / 2) > 1e-1:
                for peak in self.peaks:
                    temp = peak.copy()
                    peak[2] = math.cos(rotX) * temp[2] + 0.5 * temp[1] * math.sin(rotX)
                    peak[1] = temp[1] * math.cos(rotX) - 2 * temp[2] * math.sin(rotX)

        self.do_bias()
        self.rebuildLazer = rebuild

    def find_point_plane(self, k=[0, 0, 0], b=[0, 0, 0]):
        self.do_normal()
        if self.normal[0] * k[0] + self.normal[1] * k[1] + self.normal[2] * k[2] != 0:
            return (self.normal[0] * (self.scale * self.peaks[0][0] + self.bias[0] - b[0]) +
                    self.normal[1] * (self.scale * self.peaks[0][1] + self.bias[1] - b[1]) +
                    self.normal[2] * (self.scale * self.peaks[0][2] + self.bias[2] - b[2])) / \
                   (self.normal[0] * k[0] + self.normal[1] * k[1] + self.normal[2] * k[2])
        else:
            self.rot(rotY=0.05, rotZ=0.05)
            return self.find_point_plane(k, b)

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

        det_v = (vAB[0] * vAC[1] - vAB[1] * vAC[0])
        if det_v != 0:
            k = (vP[0] * vAC[1] - vP[1] * vAC[0]) / det_v
            f = (vAB[0] * vP[1] - vAB[1] * vP[0]) / det_v
            if 0 <= k <= 1 and 0 <= f <= 1 and k + f <= 1 and move:
                return True
            else:
                self.bias[0] = point[0]
                self.bias[1] = point[1]
                self.bias[2] = point[2]
                return True
        else:
            self.bias[0] = point[0]
            self.bias[1] = point[1]
            self.bias[2] = point[2]
            return True

    def create_new_k(self, d=[0, 0, 0]):
        self.do_normal()
        len1 = (self.normal[0] ** 2 + self.normal[1] ** 2 + self.normal[2] ** 2) ** 0.5
        v = [-self.normal[0] / len1, -self.normal[1] / len1, -self.normal[2] / len1]
        sc = v[0] * d[0] + v[1] * d[1] + v[2] * d[2]
        k = [0, 0, 0]
        eps = 1e-6
        k[0] = d[0] - 2 * v[0] * sc + eps
        k[1] = d[1] - 2 * v[1] * sc + eps
        k[2] = d[2] - 2 * v[2] * sc + eps
        return k

    def set_rebuild_lazer(self, a):
        self.rebuildLazer = a

    def rot_set(self, rotX, rotY, rotZ, rebuild=True):
        self.rotZ = rotZ
        for i in range(3):
            temp = self.peaksC[i].copy()
            self.peaks[i][0] = math.cos(rotZ) * temp[0] + temp[1] * math.sin(rotZ)
            self.peaks[i][1] = temp[1] * math.cos(rotZ) - temp[0] * math.sin(rotZ)

        self.rotY = rotY
        for peak in self.peaks:
            temp = self.peaksC[i].copy()
            self.peaks[i][2] = math.cos(rotY) * temp[2] + 0.5 * temp[0] * math.sin(rotY)
            self.peaks[i][0] = temp[0] * math.cos(rotY) - 2 * temp[2] * math.sin(rotY)

        self.rotX = rotX
        for peak in self.peaks:
            temp = self.peaksC[i].copy()
            self.peaks[i][2] = math.cos(rotX) * temp[2] + 0.5 * temp[1] * math.sin(rotX)
            self.peaks[i][1] = temp[1] * math.cos(rotX) - 2 * temp[2] * math.sin(rotX)

        self.do_bias()
        self.rebuildLazer = rebuild
