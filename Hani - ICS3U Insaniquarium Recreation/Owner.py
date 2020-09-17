import Food, random
from Food import Food
import Fish 
from Fish import Fish
import pygame
from collision import intersectsX

class Owner:
    
    def __init__(self,images):
            self.images = images
            self.current_image = images[0]
            self.x_mouse = 0
            self.y_mouse = 0
            self.max_food = 0 #for max food allowed
            self.bank_value = 500
    
    '''Updates objects mouse positions
    This function is only called on when the mouse is clicked.'''
    def mouse_pos(self): #updates mouse position
        mousePosition = pygame.mouse.get_pos()
        self.x_mouse = mousePosition[0]
        self.y_mouse = mousePosition[1]
    
    '''Checks if players mouse is on start button'''
    def press_play(self):
        if 515 >= self.x_mouse >= 230:
            if 605 >= self.y_mouse >= 570:
                return True
    
    '''Creates a food object, subtracts cost from players bank account
    First checks to see if player has enough money and their mouse is within the boundaries'''
    def feed(self,food_stor):
        self.current_image = random.choice(self.images)
        if (self.y_mouse > 90 and self.y_mouse < 590 and
        self.x_mouse > 15 and self.x_mouse < 765) and (self.max_food < 8) and self.bank_value > 4: #mouse is in the tank and bank has money
                food_stor.add(Food(self.current_image,self.x_mouse,self.y_mouse))
                self.max_food += 1
                self.bank_value -= 5
                return True
    
    '''Player can drop one more food on screen'''
    def max_food_minus(self):
        self.max_food -= 1
    
    def display_bank(self,screen,font):
        bankdigits = str(self.bank_value)
        blankspace = ' ' * (6 - len(bankdigits)) #3 space when bank value 3 digits, 4 space when 2 dig
        bank_display = font.render(blankspace + '$' + bankdigits + ' ',0,(127,255,0),(46,139,87)) #12 characters long
        screen.blit(bank_display,(667,50))
        
    def check_money(self,money_stor):
        for moneybag in money_stor:
            moneybagX = moneybag.x #get the coordinates of the bag
            moneybagY = moneybag.y
            if (moneybagX + 40 >= self.x_mouse >= moneybagX and
                moneybagY + 40 >= self.y_mouse >= moneybagY):
                moneybag.obtained()
                self.bank_value += 150 #adds money to bank
                return True #a money bag was clicked on
    
    def new_fish(self,fish_stor,fish_images):
        if 78 >= self.x_mouse >= 30: #two conditionals faster or slower than one?
            if 50 >= self.y_mouse >= 10:
                if self.bank_value >= 100:
                    fish_stor.add(Fish(fish_images,150,200))
                    self.bank_value -= 100
                    return True
    
    '''Checks to see if mouse is on menu button'''
    def pause(self):  
        '''  
        courierFont = pygame.font.SysFont("Courier", 18)
        pause_text = courierFont.render("PAUSE",1, (255,0,0), 0)
        screen.blit(pause_text, (390,326))
        pygame.draw.rect(screen, (255,255,255), (655,10,90,22), 1)
        '''
        if 745 >= self.x_mouse >= 655:
            if 32 >= self.y_mouse >= 10:
                return True
    
    '''Alien loses hp if mouse if on alien'''
    def shoot(self,alien):
        if alien.x  + alien.width> self.x_mouse > alien.x:
            if alien.y + alien.height> self.y_mouse > alien.y:
                alien.hp -= 10
                return True
    
    '''Player can purchase egg if they have enough money and mouse is on egg'''
    def egg(self):
        #pygame.draw.rect(screen,(255,255,255),(542,12,46,40))
        if 588 >= self.x_mouse >= 542:
            if 52 >= self.y_mouse >= 12:
                if self.bank_value >= 3000: #bc egg costs 3000
                    return True