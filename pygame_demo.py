##################################################
#
#   This demo is a quick build for baby smash activity -
#   It is based on pygame and intended to randomize a shape, colour or image
#   and print it to screen whenever the baby hits a key.
#   Another addition is HEB <--> RUS naming of the shape or colour or image.
#
#   The game was developed on windows10 with python 2.7, and perhaps as result
#   encountered some development sound problems:
#   1. Sound channel isn't working (not mp3, ogg or anything) - insead of sound 
#      there's an initial static but no sound - only music channel is working
#      hence sound is played with music insead of sound channle.
#   2. Music channel doesn't play queues tracks, thereofore, instead of saying shape
#      first, queueing the colour and hearing it after the shape is finished playing,
#      we don't have more than one played sound, so we randomize if the voice will 
#      say the shape's name or its colour.
#
##################################################
import os
import sys
import pygame
import argparse
import math
from datetime import datetime
from pygame.locals import *
from random import randint


MIN_SHAPE_SIZE = 100
MAX_SHAPE_SIZE = 200
MAX_TIME_DIFF_SECONDS = 2


class ColourObject():
    """
	Container class for colour - colour value and its filename
	"""
    colour = None
    filename = None	
	
    def __init__(self, colour, filename):
        self.colour = colour
        self.filename = filename

		
col_dict = { 'RED' : ColourObject( (255, 0, 0), ['sounds//red.ogg']),
             'GREEN' : ColourObject( (0, 255, 0), ['sounds//green.ogg']), 
			 'BLUE' : ColourObject( (0, 0, 255), ['sounds//blue.ogg']),
			 'YELLOW' : ColourObject( (255, 255, 0), ['sounds//yellow.ogg']),
             'WHITE' : ColourObject( (255, 255, 255), ['sounds//white.ogg']),
			 'BLACK' : ColourObject( (0, 0, 0), ['sounds//black.ogg']),
			 'PURPLE' : ColourObject( (128, 0, 128), ['sounds//purple.ogg']),
             'ORANGE' : ColourObject( (255, 128, 0), ['sounds//orange.ogg']),
 			}

shapes_dict = { 'CIRCLE' : lambda x,y,r,col: ShapeCircle(x,y,r,col),
                'TRIANGLE' : lambda x,y,r,col: ShapeTriangle(x,y,r,col),
                'RECTANGLE' : lambda x,y,r,col: ShapeRectangle(x,y,r,col),
                'PENTAGON' : lambda x,y,r,col: ShapePentagon(x,y,r,col), 		
                'STAR' : lambda x,y,r,col: ShapeStar(x,y,r,col), 		
				}		

images_dict = { 'DOG' : lambda x,y: ImageDog(x,y),
                'CAT' : lambda x,y: ImageCat(x,y),
                'DOLPHIN' : lambda x,y: ImageDolphin(x,y),
                'GOOSE' : lambda x,y: ImageGoose(x,y),
                'HORSE' : lambda x,y: ImageHorse(x,y),
                'BEAR' : lambda x,y: ImageBear(x,y),
                'APE' : lambda x,y: ImageApe(x,y),
                'TURTLE' : lambda x,y: ImageTurtle(x,y),
                'FISH' : lambda x,y: ImageFish(x,y),
                'BUTTERFLY' : lambda x,y: ImageButterfly(x,y)
			  }
				
				
__image_on_demand_dict__ = {}
							
	


def GetImage(filename):
    """
	Loads images only once by storing to global dictionary
	"""
    if (__image_on_demand_dict__.has_key(filename)) == False:
        img = pygame.image.load(filename)
        __image_on_demand_dict__[filename] = img
    return  __image_on_demand_dict__[filename]
	

def GetDots(x, y, r, n, offset=0):
    """
	Function that sets N points on a radius
	"""
    dots = []
    for idx in range(n):
        dots.append( ( int( x+r*math.cos(math.pi*2/n*(idx-1)+offset) ), int( y+r*math.sin(math.pi*2/n*(idx-1)+offset) ) ) )
    return dots
			
	
class ActivityObject(object):
    """
	Generic activity object - has location and can draw and play sound(s)
	"""
    x = 0
    y = 0
    name = None
    sounds = []

    def __init__(self, x, y, name, sounds):
        self.x = int(x)
        self.y = int(y)
        self.name = name
        self.sounds = sounds

    def Draw(self, surf):
        pass	
	
    def PlaySound(self):
	    """
	    Choose a random set of sounds and play them in queue
	    NOTE: the queue functionallity isn't working - only first track is played
	    """
	    if (self.sounds != None):
	        lst_idx = randint(0, len(self.sounds)-1)
	        snd_list = self.sounds[lst_idx]
	        pygame.mixer.music.stop()
	        for idx, snd in enumerate(snd_list):
	            if (idx == 0):
	                pygame.mixer.music.load(snd)
	                pygame.mixer.music.play()
	            else:
	                pygame.mixer.music.queue(snd)
	
	
class ShapeObject(ActivityObject):
    """
	Generic shape object
	"""
    x = 0
    y = 0
    size = 0
    col = col_dict['BLACK']

    def __init__(self, x, y, name, snd_lst, size, col):
        if (col.filename != None):
            if ((snd_lst) == None):
                snd_lst = [ col.filename ]
            else:
                snd_lst.append(col.filename)
        super(ShapeObject, self).__init__(x, y, name, snd_lst)
        self.size = size
        self.col = col

    def Draw(self, surf):
        pass	
		

class ShapeCircle(ShapeObject):
    def __init__(self, x, y, size, col):
        super(ShapeCircle, self).__init__( x, y, 'CIRCLE', [['sounds//circle.ogg']], size, col)
	
    def Draw(self, surf):
		x = self.x
		y = self.y
		r = self.size
		pygame.draw.circle(surf, self.col.colour, (x, y), r)
		pygame.draw.circle(surf, col_dict['WHITE'].colour, (x, y), r, 1)
	

class ShapeTriangle(ShapeObject):
    def __init__(self, x, y, size, col):
        super(ShapeTriangle, self).__init__(x, y, 'TRIANGLE', [['sounds//triangle.ogg']], size, col)

    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        dots = GetDots(x, y, r, 3, math.radians(30))
        pygame.draw.polygon(surf, self.col.colour, dots ) 
        pygame.draw.polygon(surf, col_dict['WHITE'].colour, dots, 1)
	

class ShapeRectangle(ShapeObject):
    def __init__(self, x, y, size, col):
        super(ShapeRectangle, self).__init__(x, y, 'RECTANGLE', [['sounds//rectangle.ogg']], size, col)

    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        dots = GetDots(x, y, r, 4, math.radians(45))
        pygame.draw.polygon(surf, self.col.colour, dots ) 
        pygame.draw.polygon(surf, col_dict['WHITE'].colour, dots, 1) 
		

class ShapePentagon(ShapeObject):
    def __init__(self, x, y, size, col):
        super(ShapePentagon, self).__init__(x, y, 'PENTAGON', [['sounds//pentagon.ogg']], size, col)

    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        dots = GetDots(x, y, r, 5, math.radians(18+180))
        pygame.draw.polygon(surf, self.col.colour, dots )
        pygame.draw.polygon(surf, col_dict['WHITE'].colour, dots, 1) 
		

class ShapeStar(ShapeObject):
    def __init__(self, x, y, size, col):
        super(ShapeStar, self).__init__(x, y, 'STAR', [['sounds//star.ogg']], size, col)

    def Draw(self, surf):
        x = self.x
        y = self.y
        r = self.size
        offset = math.radians(90)-math.pi*2/10
        dots = GetDots(x, y, r, 10, offset)					# create a 10-points poligon as base
        dots_inner = GetDots(x, y, r*0.5, 10, offset)		# create a smaller 10-points poligon as rider
        dots[::2] = dots_inner[::2]							# replace the even dots of the base with the smaller to get the edges
        pygame.draw.polygon(surf, self.col.colour, dots )
        pygame.draw.polygon(surf, col_dict['WHITE'].colour, dots, 1) 


class ImageDisplayer(ActivityObject):
    """
	Displays an image 
	"""
    name = ""
    img = None
    fliename = ""
	
    def __init__(self, x, y, name, img_filename, snd_list):
        img = GetImage(img_filename)
        x = x - img.get_width()*0.5
        y = y - img.get_height()*0.5
        super(ImageDisplayer, self).__init__(x, y, name, snd_list)
        self.filename = img_filename
    
    def Draw(self, surf):
        img = GetImage(self.filename)
        surf.blit(img, (self.x, self.y) )
        pygame.draw.rect(surf, col_dict['WHITE'].colour, (self.x, self.y, img.get_width(), img.get_height()), 1)
		

class ImageDog(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageDog, self).__init__(x, y, 'DOG', 'images//dog.jpg', [['sounds//dog.ogg']])

		
class ImageCat(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageCat, self).__init__(x, y, 'CAT', 'images//cat.jpg', [['sounds//cat.ogg']])

		
class ImageBear(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageBear, self).__init__(x, y, 'BEAR', 'images//bear.jpg', [['sounds//bear.ogg']])

		
class ImageDolphin(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageDolphin, self).__init__(x, y, 'DOLPHIN', 'images//dolphin.jpg', [['sounds//dolphin.ogg']])

		
class ImageGoose(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageGoose, self).__init__(x, y, 'GOOSE', 'images//goose.jpg', [['sounds//goose.ogg']])

		
class ImageHorse(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageHorse, self).__init__(x, y, 'HORSE', 'images//horse.jpg', [['sounds//horse.ogg']])

class ImageApe(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageApe, self).__init__(x, y, 'APE', 'images//ape.jpg', [['sounds//ape.ogg']])
		
class ImageButterfly(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageButterfly, self).__init__(x, y, 'APE', 'images//butterfly.jpg', [['sounds//butterfly.ogg']])

class ImageTurtle(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageTurtle, self).__init__(x, y, 'TURTLE', 'images//turtle.jpg', [['sounds//turtle.ogg']])
		
class ImageFish(ImageDisplayer):
    def __init__(self, x, y):
        super(ImageFish, self).__init__(x, y, 'FISH', 'images//fish.jpg', [['sounds//fish.ogg']])
			
		
def get_activity_object(max_x, max_y, max_size):
    """
    Draw a random activity (shape, ...)
    """
    p = randint(0, 1)	# random coin toss - 0 for shape, 1 for image
    if (p == 0):
        """
        Choose a shape
        """
        x = max_x*0.5
        y = max_y*0.5
        x = randint(MIN_SHAPE_SIZE*2, max_x-MIN_SHAPE_SIZE*2-1)
        y = randint(MIN_SHAPE_SIZE*2, max_y-MIN_SHAPE_SIZE*2-1)
        r = randint(MIN_SHAPE_SIZE, MIN_SHAPE_SIZE+max_size)

        col_name = col_dict.keys()[ randint(0, len(col_dict)-1) ]
        col = col_dict[col_name]
        shape_name = shapes_dict.keys()[ randint(0, len(shapes_dict)-1) ]
        new_activity = shapes_dict[shape_name](x,y,max_size,col)
		
    else:	
        """
        Choose an image
        """
        image_name = images_dict.keys()[ randint(0, len(images_dict)-1) ]
        new_activity = images_dict[image_name](max_x*0.5, max_y*0.5)	
	
    return new_activity 

	
	
def main():
    """
	Main game loop - initializes the display, pre-loads resources 
	and waits for events to activate
	"""
	
    parser = argparse.ArgumentParser(description='Baby smash game')
    parser.add_argument('--window_mode', dest='window_mode', action='store_true', default='False', 
	                    help='If set, open the display in window mode instead of full screen')					
    parser.add_argument('--delay_time', dest='delay_time', type=int, default=MAX_TIME_DIFF_SECONDS, 
	                    help='Time in seconds between click activation (default = 2sec). 0 means no minimal wait')					
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
	Main loop - waits for key and activates an activity 
	"""
    last_click_timestamp = datetime(1, 1, 1)    # Minimal timedate, just for starters
	
    while True: # main game loop
        for event in pygame.event.get():
	        if (event.type == KEYDOWN) or (event.type == MOUSEBUTTONDOWN):
			    now_time = datetime.now()
			    delta = now_time - last_click_timestamp
			    if (delta.seconds >= args.delay_time):
			        last_click_timestamp = now_time
			        pygame.draw.rect(DISPLAYSURF, col_dict['BLACK'].colour, (0, 0, max_x, max_y))        # Delete the previous screen (draw big black rect)
			        new_activity = get_activity_object(max_x, max_y, MAX_SHAPE_SIZE)
			        new_activity.Draw(DISPLAYSURF)
			        new_activity.PlaySound()

	        elif (event.type == QUIT):
	            print("Quiting")
	            pygame.quit()
	            sys.exit()   

        pygame.display.update()
	
			
		
if __name__ == '__main__':
    main()	