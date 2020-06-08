import math
import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Cube:
    def __init__(self, screen, scale=1, bias=[0, 0, 0]):
        self.peaks = [[-1, -1, -0.5], [1, 1, 0.5]]
        self.sc = screen
        self.scale = scale
        self.bias = bias
        self.rotLast = True
        self.rotXZ = 0.0
        self.rotYX = 0.0
        self.a1 = self.peaks[0].copy()
        self.b1 = [self.peaks[0][0], self.peaks[1][1], self.peaks[0][2]]
        self.c1 = [self.peaks[1][0], self.peaks[1][1], self.peaks[0][2]]
        self.d1 = [self.peaks[1][0], self.peaks[0][1], self.peaks[0][2]]

        self.a2 = [self.peaks[0][0], self.peaks[0][1], self.peaks[1][2]]
        self.b2 = [self.peaks[0][0], self.peaks[1][1], self.peaks[1][2]]
        self.c2 = self.peaks[1].copy()
        self.d2 = [self.peaks[1][0], self.peaks[0][1], self.peaks[1][2]]
        self.coordPeaks = [self.a1, self.b1, self.c1, self.d1, self.a2, self.b2, self.c2, self.d2]

        self.a1bias, self.b1bias, self.c1bias, self.d1bias = [0, 0], [0, 0], [0, 0], [0, 0]
        self.a2bias, self.b2bias, self.c2bias, self.d2bias = [0, 0], [0, 0], [0, 0], [0, 0]

    def draw(self, color=WHITE):
        if self.rotLast:
            self.a1bias = [self.bias[0] + (self.scale * self.a1[0] +
                                           (self.scale * self.a1[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                           self.bias[1] + (self.scale * self.a1[1] +
                                           (self.scale * self.a1[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]
            self.b1bias = [self.bias[0] + (self.scale * self.b1[0] +
                                           (self.scale * self.b1[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                           self.bias[1] + (self.scale * self.b1[1] +
                                           (self.scale * self.b1[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]
            self.c1bias = [self.bias[0] + (self.scale * self.c1[0] +
                                           (self.scale * self.c1[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                           self.bias[1] + (self.scale * self.c1[1] +
                                           (self.scale * self.c1[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]
            self.d1bias = [self.bias[0] + (self.scale * self.d1[0] +
                                           (self.scale * self.d1[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                           self.bias[1] + (self.scale * self.d1[1] +
                                           (self.scale * self.d1[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]

            self.a2bias = [self.bias[0] + (self.scale * self.a2[0] +
                                           (self.scale * self.a2[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                           self.bias[1] + (self.scale * self.a2[1] +
                                           (self.scale * self.a2[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]
            self.b2bias = [self.bias[0] + (self.scale * self.b2[0] +
                                           (self.scale * self.b2[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                           self.bias[1] + (self.scale * self.b2[1] +
                                           (self.scale * self.b2[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]
            self.c2bias = [self.bias[0] + (self.scale * self.c2[0] +
                                           (self.scale * self.c2[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                           self.bias[1] + (self.scale * self.c2[1] +
                                           (self.scale * self.c2[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]
            self.d2bias = [self.bias[0] + (self.scale * self.d2[0] +
                                           (self.scale * self.d2[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2),
                           self.bias[1] + (self.scale * self.d2[1] +
                                           (self.scale * self.d2[2] + 2 * self.bias[2]) * math.cos(math.pi / 4) / 2)]
            self.rotLast = False

        pygame.draw.line(self.sc, color, [self.a1bias[0], self.a1bias[1]], [self.b1bias[0], self.b1bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.b1bias[0], self.b1bias[1]], [self.c1bias[0], self.c1bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.c1bias[0], self.c1bias[1]], [self.d1bias[0], self.d1bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.d1bias[0], self.d1bias[1]], [self.a1bias[0], self.a1bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.a2bias[0], self.a2bias[1]], [self.b2bias[0], self.b2bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.b2bias[0], self.b2bias[1]], [self.c2bias[0], self.c2bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.c2bias[0], self.c2bias[1]], [self.d2bias[0], self.d2bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.d2bias[0], self.d2bias[1]], [self.a2bias[0], self.a2bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.a1bias[0], self.a1bias[1]], [self.a2bias[0], self.a2bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.b1bias[0], self.b1bias[1]], [self.b2bias[0], self.b2bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.c1bias[0], self.c1bias[1]], [self.c2bias[0], self.c2bias[1]], 1)
        pygame.draw.line(self.sc, color, [self.d1bias[0], self.d1bias[1]], [self.d2bias[0], self.d2bias[1]], 1)

    def rot(self, rotXZ=0.0, rotYX=0.0):
        if rotYX != 0.0:
            self.rotYX += rotYX
            if self.rotYX > 2 * math.pi:
                self.rotYX -= 2 * math.pi
            for peak in self.coordPeaks:
                temp = peak.copy()
                peak[0] = math.cos(rotYX) * temp[0] + temp[1] * math.sin(rotYX)
                peak[1] = temp[1] * math.cos(rotYX) - temp[0] * math.sin(rotYX)
            self.rotLast = True

        if rotXZ != 0.0:
            self.rotXZ += rotXZ
            if self.rotXZ > 2 * math.pi:
                self.rotXZ -= 2 * math.pi
            for peak in self.coordPeaks:
                temp = peak.copy()
                peak[2] = math.cos(rotXZ) * temp[2] + 0.5 * temp[0] * math.sin(rotXZ)
                peak[0] = temp[0] * math.cos(rotXZ) - 2 * temp[2] * math.sin(rotXZ)
            self.rotLast = True