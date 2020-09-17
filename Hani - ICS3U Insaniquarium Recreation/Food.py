import pygame

class Food(pygame.sprite.Sprite):
    
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.x = x
        self.y = y
        
        size = self.image.get_size()
        self.width = size[0]
        self.height = size[1]
    
    def movement(self,screen):
        self.y += 2
        screen.blit(self.image,(self.x,self.y)) #displays food
    
    def ground(self):
        if self.y > 590:
            self.kill()
            return True