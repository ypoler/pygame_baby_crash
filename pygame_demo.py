import pygame, sys
from pygame.locals import *
from random import randint



pygame.init()
#DISPLAYSURF = pygame.display.set_mode((400, 300), pygame.FULLSCREEN)
info = pygame.display.Info()

print(info)
max_x = info.current_w
max_y = info.current_h
DISPLAYSURF = pygame.display.set_mode((max_x, max_y), pygame.FULLSCREEN)
pygame.display.set_caption('Hello World!')

RED = (255, 0, 0)
pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

while True: # main game loop
    for event in pygame.event.get():
	    if event.type == KEYDOWN:
	        if event.key == K_SPACE:
      #  if event.type == QUIT:
	            pygame.quit()
	            sys.exit()
            else:
		        x = randint(0, max_x-1)
		        y = randint(0, max_y-1)
		        pygame.draw.rect(DISPLAYSURF, RED, (x, y, x+59, y+20))


    pygame.display.update()