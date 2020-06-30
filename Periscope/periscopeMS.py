import sys
import pygame
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


def draw():
    cub1.draw()
    cyl1.draw()
    mir1.draw()
    mir2.draw()
    laz.draw()

pygame.init()

sc = pygame.display.set_mode(size)
bias = [550, 350, 0]
cub1 = Cube(sc, scale=15, bias=bias)
cyl1 = Cylinder(sc, scale=10, bias=[100, 100, 0])
mir1 = Mirror(sc, scale=30, bias=[360, 350, 0])
mir2 = Mirror(sc, scale=30, bias=[360, 100, 0])
laz = Lazer(sc, st_point=bias, mir=[mir1, mir2], cyl=cyl1)
laz.dot(index=0)

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
            elif event.key == pygame.K_KP_PLUS:
                cyl1.bias[2] = min(cyl1.bias[2] + 5, 80)
            elif event.key == pygame.K_KP_MINUS:
                cyl1.bias[2] = max(cyl1.bias[2] - 5, -80)
            cyl1.rotLast = True
            laz.rebuild_lazer()
    sc.fill(BLACK)
    draw()
    pygame.display.flip()
