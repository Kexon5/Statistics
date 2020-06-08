import sys
import pygame
import math
from MStat.Cube import Cube
from MStat.Cylinder import Cylinder
from MStat.Lazer import Lazer
from MStat.Mirror import Mirror

size = [640, 480]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def rot():
    k = [(mir2.bias[0] + 2 * cub1.bias[0])/3, (mir2.bias[1] + 2 * cub1.bias[1])/3, 0]
    vP = [k[0] - mir1.bias[0], k[1] - mir1.bias[1], 0]
    n = (vP[0] ** 2 + vP[1] ** 2) ** 0.5
    vP = [vP[0] / n, vP[1] / n, 0]
    alpha = math.acos((mir1.normal[0] * vP[0] + mir1.normal[1] * vP[1]) / mir1.normalize())

    mir1.rot(rotZ=-alpha)

    k = [(cyl1.bias[0] + mir1.bias[0]) / 2, (mir1.bias[1] + cyl1.bias[1]) / 2, 0]
    vP = [k[0] - mir2.bias[0], k[1] - mir2.bias[1], 0]
    n = (vP[0] ** 2 + vP[1] ** 2) ** 0.5
    vP = [vP[0] / n, vP[1] / n, 0]
    alpha = math.acos((mir2.normal[0] * vP[0] + mir2.normal[1] * vP[1]) / mir2.normalize())
    mir2.rot(rotZ=alpha)
    #cyl1.rot(rotXZ=math.pi / 4)


def draw():
    cub1.draw()
    cyl1.draw()
    laz.draw()
    mir1.draw()
    mir2.draw()


pygame.init()

sc = pygame.display.set_mode(size)
bias = [550, 350, 10]
cub1 = Cube(sc, scale=15, bias=bias)
cyl1 = Cylinder(sc, scale=10, bias=[100, 100, 0])
mir1 = Mirror(sc, scale=30, bias=[400, 350, 10])
mir2 = Mirror(sc, scale=30, bias=[360, 80, 10])
rot()
laz = Lazer(sc, st_point=bias, mir=[mir1, mir2], cyl=cyl1)
laz.dot(index=0)
c = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cyl1.bias[0] = max(cyl1.bias[0] - 5, 20)
            elif event.key == pygame.K_RIGHT:
                cyl1.bias[0] = min(cyl1.bias[0] + 5, 280)
            elif event.key == pygame.K_UP:
                cyl1.bias[1] = max(cyl1.bias[1] - 5, 20)
            elif event.key == pygame.K_DOWN:
                cyl1.bias[1] = min(cyl1.bias[1] + 5, 300)
                #print(laz.d[2])
            mir2.set_rebuild_lazer(True)
            cyl1.rotLast = True
    sc.fill(BLACK)
    draw()

    if c == 100:
        #mir1.rot(rotX=0.05)
        c = -1
    c += 1
    pygame.display.flip()
