import os
import sys
import pygame
import argparse
from pygame.locals import *
from random import randint


MAX_ACTIVITY = 3	
MIN_SHAPE_SIZE = 100
COL_WHITE = (255, 255, 255)
COL_BLACK = (0, 0, 0)

col_dict = { 'RED' : (255, 0, 0),
             'GREEN' : (0, 255, 0), 
			 'BLUE' : (0, 0, 255),
			 'YELLOW' : (255, 255, 0),
             'WHITE' : (255, 255, 255),
             'ORANGE' : (255, 165, 0)  
 			}

			
	
def play_sound(filename):
    """
	Play a sound
	"""
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)	


	
class ShapeObject:
    """
	Generic shape object
	"""
    x = 0
    y = 0
    size = 0
    col = COL_BLACK
    name = ""

    def __init__(self, x, y, size, col):
        self.x = x
        self.y = y
        self.size = size
        self.col = col

    def Draw(self, surf):
        pass	



class ShapeCircle(ShapeObject):
    name = "circle"

    def Draw(self, surf):
		x = self.x
		y = self.y
		r = self.size
		pygame.draw.circle(surf, self.col, (x, y), r)
		pygame.draw.circle(surf, COL_WHITE, (x, y), r+1, 1)
	

class ShapeTriangle(ShapeObject):
    name = "triangle"

    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        pygame.draw.polygon(surf, self.col, ((x, y-r), (x+r*0.86, y+r*0.5), (x-r*0.86, y+r*0.5)) )
        pygame.draw.polygon(surf, COL_WHITE, ((x, y-1-r), (x+1+r*0.86, y+1+r*0.5), (x-1-r*0.86, y+1+r*0.5)), 1 )
	

class ShapeRectangle(ShapeObject):
    name = "rectangle"

    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        pygame.draw.rect(surf, self.col, (x-r*0.707, y-r*0.707, r*0.707*2, r*0.707*2) )
        pygame.draw.rect(surf, COL_WHITE, (x-r*0.707-1, y-r*0.707-1, r*0.707*2+2, r*0.707*2+2), 1 )
	

def draw_random_activity(surf, max_x, max_y, max_size, sound_list):
    """
	Draw a random activity (shape, ...)
	"""
	
    pygame.draw.rect(surf, COL_BLACK, (0, 0, max_x, max_y))        # Delete the previous screen (draw big black rect)
	
    x = randint(MIN_SHAPE_SIZE*2, max_x-MIN_SHAPE_SIZE*2-1)
    y = randint(MIN_SHAPE_SIZE*2, max_y-MIN_SHAPE_SIZE*2-1)
    r = randint(MIN_SHAPE_SIZE, MIN_SHAPE_SIZE+max_size)
    col = col_dict.values()[ randint(0, len(col_dict)-1) ]
    activity = randint(0, MAX_ACTIVITY-1)
    
    sound_file = sound_list[randint(0, len(sound_list)-1)]
	
    new_shape = ShapeTriangle(x, y, r, col)
	
    if (activity == 0):
	    new_shape = ShapeCircle(x, y, r, col)
    elif (activity == 1):
	    new_shape = ShapeRectangle(x, y, r, col)
    elif (activity == 2):
	    new_shape = ShapeTriangle(x, y, r, col)
		
    new_shape.Draw(surf)
    play_sound(sound_file)	


			
def main():
    """
	Main game loop - initializes the display, pre-loads resources 
	and waits for events to activate
	"""
	
    parser = argparse.ArgumentParser(description='Baby smash game')
    parser.add_argument('--window_mode', dest='window_mode', action='store_true', default='False', 
	                    help='If set, open the display in window mode instead of full screen')					
    args = parser.parse_args()
	
	
    """
    Initialize the display settings based on the display device and args
    """
    pygame.init()
    info = pygame.display.Info()
    max_x = info.current_w
    max_y = info.current_h
    if (args.window_mode == True):
        max_x = int(max_x*0.75)
        max_y = int(max_y*0.75)
        DISPLAYSURF = pygame.display.set_mode( (max_x, max_y) )
    else:
        DISPLAYSURF = pygame.display.set_mode( (max_x, max_y), pygame.FULLSCREEN)

    pygame.display.set_caption('Baby Smash')

	
    """
    Get the sounds list
    """
    sound_list = []
    for file in os.listdir("sounds"):
        if file.endswith(".mp3"):
            sound_list.append(os.path.join("sounds", file))
		
		
		
	"""
	Main loop - waits for key and activates an activity 
	"""
    while True: # main game loop
        for event in pygame.event.get():
	        if (event.type == KEYDOWN):
		        draw_random_activity(DISPLAYSURF, max_x, max_y, 200, sound_list)

	        elif (event.type == QUIT):
	            print("Quiting")
	            pygame.quit()
	            sys.exit()   

        pygame.display.update()
	
			
		
if __name__ == '__main__':
    main()	