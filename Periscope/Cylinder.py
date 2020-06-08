import math
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Cylinder:
    def __init__(self, screen, scale=1, bias=[0, 0, 0]):
        self.peaks = [[-2, -1.5, -0.75], [2, 1.5, 0.75]]
        self.sc = screen
        self.scale = scale
        self.bias = bias
        self.bias[0] = min(self.bias[0], 250)
        self.bias[1] = min(self.bias[1], 200)
        self.rotLast = True
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

        self.k_max = [0, 0, 0]
        self.pointsCenter = [[0, 0, 0], [0, 0, 0]]
        self.seekCenters()

    def getCentersAndCoef(self):
        self.seekCenters()
        return self.pointsCenter, self.k_max

    def seekCenters(self):
        p1 = [self.bias[0] + self.scale * (self.a1[0] + self.b2[0]) / 2,
              self.bias[1] + self.scale * (self.a1[1] + self.b2[1]) / 2,
              self.bias[2] + self.scale * (self.a1[2] + self.b2[2]) / 2]
        p2 = [self.bias[0] + self.scale * (self.d1[0] + self.c2[0]) / 2,
              self.bias[1] + self.scale * (self.d1[1] + self.c2[1]) / 2,
              self.bias[2] + self.scale * (self.d1[2] + self.c2[2]) / 2]
        if (p1[0] - 640) ** 2 + (p1[1] - 480) ** 2 < (p2[0] - 640) ** 2 + (p2[1] - 480) ** 2:
            self.pointsCenter = [p1, p2]
        else:
            self.pointsCenter = [p2, p1]

        length = self.pointsCenter[0][0] - self.pointsCenter[1][0]
        r = self.scale * self.peaks[1][1]
        self.k_max = [1, abs(r / length), abs(r / length)]

    def draw(self, color=BLUE):
        if self.rotLast:
            self.seekCenters()
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

        point1 = [min((self.a1bias[0] + self.a2bias[0]) / 2, (self.a1bias[0] + self.b1bias[0]) / 2,
                      (self.b2bias[0] + self.a2bias[0]) / 2, (self.b2bias[0] + self.b1bias[0]) / 2),
                  min((self.a1bias[1] + self.a2bias[1]) / 2, (self.a1bias[1] + self.b1bias[1]) / 2,
                      (self.b2bias[1] + self.a2bias[1]) / 2, (self.b2bias[1] + self.b1bias[1]) / 2)]
        point2 = [max((self.a1bias[0] + self.a2bias[0]) / 2, (self.a1bias[0] + self.b1bias[0]) / 2,
                      (self.b2bias[0] + self.a2bias[0]) / 2, (self.b2bias[0] + self.b1bias[0]) / 2),
                  max((self.a1bias[1] + self.a2bias[1]) / 2, (self.a1bias[1] + self.b1bias[1]) / 2,
                      (self.b2bias[1] + self.a2bias[1]) / 2, (self.b2bias[1] + self.b1bias[1]) / 2)]
        if abs(point2[0] - point1[0]) > 2 and abs(point2[1] - point1[1]) > 2:
            pygame.draw.ellipse(self.sc, color,
                                [point1[0], point1[1], abs(point2[0] - point1[0]), abs(point2[1] - point1[1])], 1)
        point1 = [min((self.c1bias[0] + self.c2bias[0]) / 2, (self.c1bias[0] + self.d1bias[0]) / 2,
                      (self.d2bias[0] + self.c2bias[0]) / 2, (self.d2bias[0] + self.d1bias[0]) / 2),
                  min((self.c1bias[1] + self.c2bias[1]) / 2, (self.c1bias[1] + self.d1bias[1]) / 2,
                      (self.d2bias[1] + self.c2bias[1]) / 2, (self.d2bias[1] + self.d1bias[1]) / 2)]
        point2 = [max((self.c1bias[0] + self.c2bias[0]) / 2, (self.c1bias[0] + self.d1bias[0]) / 2,
                      (self.d2bias[0] + self.c2bias[0]) / 2, (self.d2bias[0] + self.d1bias[0]) / 2),
                  max((self.c1bias[1] + self.c2bias[1]) / 2, (self.c1bias[1] + self.d1bias[1]) / 2,
                      (self.d2bias[1] + self.c2bias[1]) / 2, (self.d2bias[1] + self.d1bias[1]) / 2)]
        if abs((self.c2bias[1] + self.c1bias[1]) / 2 - (self.d2bias[1] + self.d1bias[1]) / 2) > 2 \
                and abs(self.d2bias[0] - self.d1bias[0]) > 2:
            pygame.draw.ellipse(self.sc, color,
                                [point1[0], point1[1], abs(point2[0] - point1[0]), abs(point2[1] - point1[1])], 1)

        pygame.draw.line(self.sc, color, [(self.b1bias[0] + self.a1bias[0]) / 2, (self.b1bias[1] + self.a1bias[1]) / 2],
                         [(self.c1bias[0] + self.d1bias[0]) / 2, (self.c1bias[1] + self.d1bias[1]) / 2], 1)
        pygame.draw.line(self.sc, color, [(self.a2bias[0] + self.a1bias[0]) / 2, (self.a2bias[1] + self.a1bias[1]) / 2],
                         [(self.d2bias[0] + self.d1bias[0]) / 2, (self.d2bias[1] + self.d1bias[1]) / 2], 1)
        pygame.draw.line(self.sc, color, [(self.c2bias[0] + self.c1bias[0]) / 2, (self.c2bias[1] + self.c1bias[1]) / 2],
                         [(self.b2bias[0] + self.b1bias[0]) / 2, (self.b2bias[1] + self.b1bias[1]) / 2], 1)
        pygame.draw.line(self.sc, color, [(self.b2bias[0] + self.a2bias[0]) / 2, (self.b2bias[1] + self.a2bias[1]) / 2],
                         [(self.c2bias[0] + self.d2bias[0]) / 2, (self.c2bias[1] + self.d2bias[1]) / 2], 1)

    def rot(self, rotYX=0.0):
        if rotYX != 0.0:
            self.rotYX += rotYX
            if self.rotYX > 2 * math.pi:
                self.rotYX -= 2 * math.pi
            for peak in self.coordPeaks:
                temp = peak.copy()
                peak[0] = math.cos(rotYX) * temp[0] + temp[1] * math.sin(rotYX)
                peak[1] = temp[1] * math.cos(rotYX) - temp[0] * math.sin(rotYX)
            self.rotLast = True
