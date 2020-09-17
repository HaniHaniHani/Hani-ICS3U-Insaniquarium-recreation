import pygame

class Money(pygame.sprite.Sprite):
    
    def __init__(self,image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image #image of money
        self.x = x 
        self.y = y
        
        size = self.image.get_size()
        self.width = size[0]
        self.height = size[1]
    
    def movement(self):
        if self.y < 590:
            self.y += 2 #moves down
    
    def obtained(self):
        self.kill()