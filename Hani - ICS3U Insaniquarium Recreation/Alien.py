import pygame

class Alien(pygame.sprite.Sprite):
    
    screen = (780,657)
    
    def __init__(self,images, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.current_image = self.images[0]
        size = self.current_image.get_size()
        self.width = size[0]
        self.height = size[1] - 10
        self.x = x
        self.y = y
        self.target = None
        self.hp = 430
    
    def eat_movement(self):
        speedH = 2 #horizontal speed
        speedV = 1 #vertical speed
        food = self.target
        '''
        if abs(self.y - food.y) < 3:
            speedV = 1 #so fish does not keep going over & under food
        if abs(self.y - food.y) < 3:
            speedH = 1

        else:'''
        if self.x + 10 > food.x -5: #numbers are added to conditionals to allign fish with alien mouth
            self.x -= speedH
            if self.x - food.x != 1: #image will not jitter when fish is close to food
                self.current_image = self.images[0]
        elif self.x + 75 < food.x +15:
            self.x += speedH
            if food.x - self.x != 1:
                self.current_image = self.images[1]
        else:
            self.x -= 1
            
        if self.y + 35 > food.y: #adds 35 so mouth meets fish
            self.y -= speedV
        elif self.y + 35 < food.y:
            self.y += speedV
        else:
            self.y += 1
        
        if self.y + 120 > 590: #y boundaries, 105 is added so tail doesn't go off screen
            self.y = 590 - 120
        if self.y < 90:
            self.y = 90
        #x boundary unneeded because alien x depends on fish x and fish x wont go off screen
            
    def set_target(self,fish):
        if self.target == None:
            self.target = fish
            return True
        else:
            return False