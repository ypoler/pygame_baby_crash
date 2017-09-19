import os
import sys
import pygame
from pygame.locals import *
from random import randint


MAX_ACTIVITY = 3	
MIN_SHAPE_SIZE = 100
COL_WHITE = (255, 255, 255)
COL_BLACK = (0, 0, 0)

COLOR_ARR = [ (255, 0, 0), # R
              (0, 255, 0), # G
			  (0, 0, 255), # B
			  (255, 255, 0), # Yellow
              (255, 255, 255), #white
              (255, 165, 0)  # Orange
 			  ]

def draw_circle(surf, x, y, r, col):
    """
    Draws a circle
    """
    pygame.draw.circle(surf, col, (x, y), r)
    pygame.draw.circle(surf, COL_WHITE, (x, y), r+1, 1)


def draw_rect(surf, x, y, w, h, col):
    """
    Draws a rectangle
    """
    pygame.draw.rect(surf, col, (x, y, w, h))
    pygame.draw.rect(surf, COL_WHITE, (x-1, y-1, w+2, h+2), 1)


def draw_triangle(surf, x, y, r, col):
    """
    Draws a triangle (all sides are same, all 60 degrees
    """	
    pygame.draw.polygon(surf, col, ((x, y-r), (x+r*0.86, y+r*0.5), (x-r*0.86, y+r*0.5)) )
    pygame.draw.polygon(surf, COL_WHITE, ((x, y-1-r), (x+1+r*0.86, y+1+r*0.5), (x-1-r*0.86, y+1+r*0.5)), 1 )

	
def play_sound(filename):
    """
	Play a sound
	"""
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)	
	

def draw_random_activity(surf, max_x, max_y, max_size, sound_list):
    """
	Draw a random activity (shape, ...)
	"""
	
    pygame.draw.rect(surf, COL_BLACK, (0, 0, max_x, max_y))        # Delete the previous screen (draw big black rect)
	
    x = randint(MIN_SHAPE_SIZE*2, max_x-MIN_SHAPE_SIZE*2-1)
    y = randint(MIN_SHAPE_SIZE*2, max_y-MIN_SHAPE_SIZE*2-1)
    r = randint(MIN_SHAPE_SIZE, MIN_SHAPE_SIZE+max_size)
    col = COLOR_ARR[ randint(0, len(COLOR_ARR)-1) ] # (255, 0, 0)
    activity = randint(0, MAX_ACTIVITY-1)
    
    sound_file = sound_list[randint(0, len(sound_list)-1)] #"sounds\Jump-SoundBible.com-1007297584.mp3"
	
    if (activity == 0):
        draw_circle(surf, x, y, r, col)
    elif (activity == 1):
        draw_rect(surf, x, y, r, randint(MIN_SHAPE_SIZE, MIN_SHAPE_SIZE+r-1), col)
    elif (activity == 2):
        draw_triangle(surf, x, y, r, col)
		
    play_sound(sound_file)	

		
pygame.init()
#DISPLAYSURF = pygame.display.set_mode((400, 300), pygame.FULLSCREEN)
info = pygame.display.Info()

print(info)
max_x = info.current_w
max_y = info.current_h
DISPLAYSURF = pygame.display.set_mode((max_x, max_y), pygame.FULLSCREEN)
pygame.display.set_caption('Hello World!')

sound_list = []
for file in os.listdir("sounds"):
    if file.endswith(".mp3"):
        sound_list.append(os.path.join("sounds", file))
		
while True: # main game loop
    for event in pygame.event.get():
	    if (event.type == KEYDOWN):
		    draw_random_activity(DISPLAYSURF, max_x, max_y, 200, sound_list)

	    elif (event.type == QUIT):
	        print("Quiting")
	        pygame.quit()
	        sys.exit()   

    pygame.display.update()