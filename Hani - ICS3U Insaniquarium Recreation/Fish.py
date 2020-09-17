import random, pygame, Money
from Money import *

class Fish(pygame.sprite.Sprite): #inherits from
    
    screen = (780,657)
    
    def __init__(self,images,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.current_image = self.images[0]
        size = self.current_image.get_size()
        self.width = size[0]
        self.height = size[1] - 20
        self.x = x 
        self.y = y
        self.stomach = 0 #how much fish has eaten
        self.target = None
        
        #random movement generator
        self.last_keyRL = 'R'
        self.last_keyUD = 'U'
        self.distancelengthRL = 0
        self.distancelengthUD = 0
    
    
    def movement(self,speed=2):
        if self.target == None:
            self.idle_movement(speed=2)
        else:
            self.eat_movement()
            
            
    '''Fish swimming
    Fish will travel in given direction for a total number of frames based on the random number generated.'''
    def idle_movement(self,speed=2): #trying to create natural movement
        direction_listRL = ('R','L')
        direction_listUD = ('U','D','N','N','N','N','N')
        
        if self.distancelengthRL <= 0:
            self.last_keyRL = random.choice(direction_listRL)
            self.distancelengthRL = random.randint(100,600)
        if self.distancelengthUD <= 0:
            self.last_keyUD = random.choice(direction_listUD)
            self.distancelengthUD = random.randint(0,10)
            
        if self.last_keyRL == 'R':
            self.x += speed
            self.current_image = self.images[1]
        elif self.last_keyRL == 'L':
            self.x -= speed
            self.current_image = self.images[0]
        self.distancelengthRL -= 1
        
        if self.last_keyUD == 'U':
            self.y -= speed
        elif self.last_keyUD == 'D':
            self.y += speed
        self.distancelengthUD -= 1
        self.screen_boundaries()
    
    
    def eat_movement(self):
        speedH = 2 #pixel movements per frame horizontally
        speedV = 3 #pixel movements per frame vertically
        food = self.target #the food its chasing
        
        if abs(self.y - food.y) < 3:
            speedV = 1 #so fish does not keep going over & under food
        if abs(self.y - food.y) < 3:
            speedH = 1
        
        if food.y > 590: #checks if food dissapeared
            self.target = None
            self.distancelengthUD = 200
            self.last_keyUD = 'U'
        else:
            if self.x > food.x:
                self.x -= speedH
                if self.x - food.x != 1: #image will not jitter when fish is close to food
                    self.current_image = self.images[0]
            elif self.x < food.x:
                self.x += speedH
                if food.x - self.x != 1:
                    self.current_image = self.images[1]
                
            if self.y > food.y:
                self.y -= speedV
            elif self.y < food.y:
                self.y += speedV
        
    '''Reassigns coordinates if fish exceeds boundaries'''
    def screen_boundaries(self):
        if self.x < 15:
            self.last_keyRL = 'R'
            self.distancelengthRL = 150
        if self.x + self.width > 775:
            self.last_keyRL = 'L'
            self.distancelengthRL = 150
        if self.y < 90:
            self.last_keyUD = 'D'
            self.distancelengthUD = 200
        elif self.y + self.height > 590:
            self.last_keyUD = 'U'
            self.distancelengthUD = 200
    
    '''When fish is fed ten pellets, they will drop food. '''
    def fed(self,money_stor,money_image):
        self.stomach += 1
        if self.stomach == 10:
            self.stomach = 0 #resets stomach back to 0
            money_stor.add(Money(money_image,self.x,self.y))
        self.target = None
    
    '''Fish coordinates decrease or increase depending on the coordinates of the alien (unused function) '''
    def run_away(self,alien): #fish swims away from alien
        
        #opposite operations to eat_movement()
        speedH = 1
        speedV = 1
        
        
        if self.x > alien.x:
            self.x += speedH
            if self.x - alien.x != 1: #image will not jitter when fish is close to alien
                self.current_image = self.images[1]
        elif self.x < alien.x:
            self.x -= speedH
            if alien.x - self.x != 1:
                self.current_image = self.images[0]
                
        if abs(self.y - alien.y) < 3 and self.y > 300:
            self.y -= speedV
        elif abs(self.y - alien.y) < 3 and self.y < 300:
            self.y += speedV
        
        elif self.y >= alien.y:
            self.y += speedV
        elif self.y < alien.y:
            self.y -= speedV
        
        '''Screen boundaries
        if fish exits boundaries, coordinates will be reassigned'''
        if self.x < 14: 
            self.x = 14
        elif self.x + self.width > 760:
            self.x = 760 - self.width
        if self.y < 90:
            self.y = 90
        elif self.y + self.height > 580:
            self.y = 580
        