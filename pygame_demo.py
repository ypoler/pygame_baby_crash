import os
import sys
import pygame
import argparse
import math
from pygame.locals import *
from random import randint


MIN_SHAPE_SIZE = 100
MAX_SHAPE_SIZE = 200

ACTIVITY_SOUND_MODE_RANDOM = 1


col_dict = { 'RED' : (255, 0, 0),
             'GREEN' : (0, 255, 0), 
			 'BLUE' : (0, 0, 255),
			 'YELLOW' : (255, 255, 0),
             'WHITE' : (255, 255, 255),
			 'BLACK' : (0, 0, 0),
			 'PURPLE' : (128, 0, 128),
             'ORANGE' : (255, 128, 0)  
 			}

shapes_dict = { 'CIRCLE' : lambda x,y,r,col: ShapeCircle(x,y,r,col),
                'TRIANGLE' : lambda x,y,r,col: ShapeTriangle(x,y,r,col),
                'RECTANGLE' : lambda x,y,r,col: ShapeRectangle(x,y,r,col),
                'PENTAGON' : lambda x,y,r,col: ShapePentagon(x,y,r,col), 		
                'STAR' : lambda x,y,r,col: ShapeStar(x,y,r,col), 		
				}		
			
sound_list_random_fx = []			
			
	
	

def GetDots(x, y, r, n, offset=0):
    dots = []
    for idx in range(n):
        dots.append( ( x+r*math.cos(math.pi*2/n*(idx-1)+offset), y+r*math.sin(math.pi*2/n*(idx-1)+offset) ) )
    return dots
	
class ShapeObject:
    """
	Generic shape object
	"""
    x = 0
    y = 0
    size = 0
    col = col_dict['BLACK']

    def __init__(self, x, y, size, col):
        self.x = x
        self.y = y
        self.size = size
        self.col = col

    def Draw(self, surf):
        pass	
		


class ShapeCircle(ShapeObject):
    def Draw(self, surf):
		x = self.x
		y = self.y
		r = self.size
		pygame.draw.circle(surf, self.col, (x, y), r)
		pygame.draw.circle(surf, col_dict['WHITE'], (x, y), r, 1)
	

class ShapeTriangle(ShapeObject):
    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        dots = GetDots(x, y, r, 3, math.radians(30))
        pygame.draw.polygon(surf, self.col, dots ) 
        pygame.draw.polygon(surf, col_dict['WHITE'], dots, 1)
	

class ShapeRectangle(ShapeObject):
    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        dots = GetDots(x, y, r, 4, math.radians(45))
        pygame.draw.polygon(surf, self.col, dots ) 
        pygame.draw.polygon(surf, col_dict['WHITE'], dots, 1) 
		

class ShapePentagon(ShapeObject):
    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        dots = GetDots(x, y, r, 5, math.radians(18+180))
        pygame.draw.polygon(surf, self.col, dots )
        pygame.draw.polygon(surf, col_dict['WHITE'], dots, 1) 
		

class ShapeStar(ShapeObject):
    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        offset = math.radians(90)-math.pi*2/10
        dots = GetDots(x, y, r, 10, offset)					# create a 10-points poligon as base
        dots_inner = GetDots(x, y, r*0.5, 10, offset)		# create a smaller 10-points poligon as rider
        dots[::2] = dots_inner[::2]							# replace the even dots of the base with the smaller to get the edges
        pygame.draw.polygon(surf, self.col, dots )
        pygame.draw.polygon(surf, col_dict['WHITE'], dots, 1) 


		


		

def get_activity_object(max_x, max_y, max_size):
    """
	Draw a random activity (shape, ...)
	"""
    x = randint(MIN_SHAPE_SIZE*2, max_x-MIN_SHAPE_SIZE*2-1)
    y = randint(MIN_SHAPE_SIZE*2, max_y-MIN_SHAPE_SIZE*2-1)
    r = randint(MIN_SHAPE_SIZE, MIN_SHAPE_SIZE+max_size)

    col_name = col_dict.keys()[ randint(0, len(col_dict)-1) ]
    shape_name = shapes_dict.keys()[ randint(0, len(shapes_dict)-1) ]

    col = col_dict[col_name]
    new_shape = shapes_dict[shape_name](x,y,r,col)
	
    return new_shape 



def PlaySoundForActivity(mode, activityObj):
    def play_sound(filename):
        """
	    Play a sound
	    NOTE: uses music instead of sound since there seems to be a 
	    problem with the channel/sound in windows 10, python 2.7 - however, music does work
	    """
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(0)	

    """
	Select the sound(s) to play for the given activity that was chosen 
	"""
    if (mode == ACTIVITY_SOUND_MODE_RANDOM):
        play_sound(sound_list_random_fx[randint(0, len(sound_list_random_fx)-1)])	



def InitializeSoundList():
    """
    Initializes the first sound list for random FX
    """
    for file in os.listdir("sounds"):
        if file.endswith(".mp3"):
            filename = os.path.join("sounds", file)
            sound_list_random_fx.append(filename)

	
	
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
    InitializeSoundList()
	
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
	Main loop - waits for key and activates an activity 
	"""
    while True: # main game loop
        for event in pygame.event.get():
	        if (event.type == KEYDOWN) or (event.type == MOUSEBUTTONDOWN):
	            pygame.draw.rect(DISPLAYSURF, col_dict['BLACK'], (0, 0, max_x, max_y))        # Delete the previous screen (draw big black rect)
	            new_activity = get_activity_object(max_x, max_y, MAX_SHAPE_SIZE)
	            new_activity.Draw(DISPLAYSURF)
	            PlaySoundForActivity(ACTIVITY_SOUND_MODE_RANDOM, new_activity)

	        elif (event.type == QUIT):
	            print("Quiting")
	            pygame.quit()
	            sys.exit()   

        pygame.display.update()
	
			
		
if __name__ == '__main__':
    main()	