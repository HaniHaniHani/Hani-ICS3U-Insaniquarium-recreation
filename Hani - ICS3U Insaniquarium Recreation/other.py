import random 
import Money
from Money import Money
import pygame

def supply_drop(money_stor,money_image):
    n = random.randint(1,600)
    if n == 8:
        money_stor.add(Money(money_image,random.randint(20,760),random.randint(90,110)))
        
def playSound(var):
    var.stop()
    var.play()
    
def playMusic(music):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()