import pygame, random, sys, Fish, Owner, Food, Alien, collision, Money, other #imports functions from other fiels
from Owner import Owner 
from Food import Food 
from Fish import Fish 
from Alien import Alien
from Money import Money
from collision import *
from other import supply_drop, playSound, playMusic
from pygame.locals import *
from threading import Timer

flags = FULLSCREEN | DOUBLEBUF #supposed to make the program faster

#add egg piece
#finish project proposal
#game over when all fishes die

# Initialize PyGame 
pygame.init()
pygame.mixer.init()
screenX,screenY = 780, 657
windowSize = (screenX, screenY)
screen = pygame.display.set_mode(windowSize)
screen.set_alpha(None)


'''Files are loaded and containers are created.
This includes the soundtrack, miscellanious sounds, and images.
Containers will holder objects and sprites.'''
clock = pygame.time.Clock()
pygame.mouse.set_visible(1) #sets mouse as visible 1 = True

#https://scratch.mit.edu/projects/156552692/#editor some audio was obtained from this source
alarm = pygame.mixer.Sound("alarm.wav") #1.6sescs
warning = pygame.mixer.Sound("alienbattlewarning.wav") #bit over 10 secs
battle = pygame.mixer.Sound("alienbattle.wav") #battle music

click = pygame.mixer.Sound("click.wav")
drop_food = pygame.mixer.Sound("drop_food.wav") #food drop sound
slurp = pygame.mixer.Sound("slurp.wav") #fish eat food sound
guppyspawn = pygame.mixer.Sound("guppyspawn.wav") #guppy spawn sound
points = pygame.mixer.Sound("points.wav") #collect money sound
chomp = pygame.mixer.Sound("chomp.wav") #alien eats fish sound
laser = pygame.mixer.Sound("laser.wav") #when player successfully shoots alien
aliendeath = pygame.mixer.Sound("aliendeath.wav") #alien dies
roar = pygame.mixer.Sound("roar.wav") #alien spawn sound
applause = pygame.mixer.Sound("applause.wav")

introscreen = pygame.image.load("intro.png") #introscreen background picture
aquarium1 = pygame.image.load("aquarium1.jpg")
aquarium2 = pygame.image.load("aquarium2.jpg")
egg = pygame.image.load("egg.JPG")
guppy1 = pygame.image.load("guppy1.png") #37 x 31, left dir
guppy2 = pygame.image.load("guppy2.png") #right dir
kfc = pygame.image.load("chicken.png")
pizza = pygame.image.load("pizza.png")
icecream = pygame.image.load("icecream.png")
moneybag = pygame.image.load("money.png")
alien1 = pygame.image.load("alien1.png") #104 x 147 , left dir
alien2 = pygame.image.load("alien2.png") #right dir
gameover = pygame.image.load("gameover.png")
crossh = pygame.image.load("crosshair.png")
winpic = pygame.image.load("win.png")

courierFont = pygame.font.SysFont("Courier", 18)
mpFont = pygame.font.SysFont("Myriad Pro", 30)

'''Stores all objects and sprites created in the game.
pygame.sprite.Group() allows pygame functions to be used on the objects.
Coordinates of images are properties of all objects.'''
food_storage = pygame.sprite.Group() #holds food sprites
fishies = pygame.sprite.Group() #holds fish sprites
moneies = pygame.sprite.Group() #holds money sprites
aliens = pygame.sprite.Group()

#create objects
player = Owner([kfc,pizza,icecream]) #allows user interaction
introText = mpFont.render('''   HANI     ICS3U     P. Cugliari   ''',1,(0,0,0),(255,255,255)) #text at bottom of first screen

#variables
ct_speed = 30 #maximum frames per second

'''The entire game is held in a while True loop so that players can play again.'''
while True:
    aliens.add(Alien([alien1,alien2],400,200)) #creates an alien and adds to container
    fishies.add(Fish([guppy1,guppy2],200,200)) #creates a fish and adds to container
    
    '''These bools are used for breaking loops.'''
    alarm_s = True
    warning_s = True
    interval_s = False
    battle_coming = False
    a_w_interval = 0
    shot = False
    time_paused = 0
    clicked0 = False
    win = False
    
    '''First part - Introscreen '''
    while True:
        for event in pygame.event.get():
            #pygame.event.set_allowed((QUIT,MOUSEBUTTONUP))
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                player.mouse_pos() #only gets mouse position when user clicks
                if player.press_play():
                    clicked0 = True
        
        if clicked0:
            clicked0 = False #resets variable for next time
            playSound(click)
            break
        
        screen.blit(introscreen,(0,0))
        #pygame.draw.rect(screen, (0,0,0), (230,570,285,35),0)
        screen.blit(introText,(220,630))
        pygame.display.update()
        clock.tick(ct_speed)  
    
    #first part - taking care of the fish
    soundtrack = pygame.mixer.music.load("tank1music.wav")
    pygame.mixer.music.play(3)  #song loops 3 times
    
    
    '''Second Part - Raising your fish'''
    while True:
        #transition to battle
        if pygame.mixer.music.get_pos() > 10000 and battle_coming: #breaks loop, alien battle starts
            pygame.mixer.music.load("alienbattle.wav") #loads music for battle
            pygame.mixer.music.play(5) #plays music for battle, loops 5 times
            #ct_speed = 40
            break
    
        elif a_w_interval > 30 and warning_s:
            alarm_s = False #wont enter first conditional again
            warning_s = False #wont enter this conditional again so music wont repeat
            pygame.mixer.music.load("alienbattlewarning.wav")
            pygame.mixer.music.play()
            battle_coming = True
    
        elif interval_s:
            a_w_interval += 1
            
        elif pygame.mixer.music.get_pos() - time_paused > 60000 and alarm_s: #based on time since music began
            pygame.mixer.music.stop() #alien warning at 60 seconds
            playSound(alarm) #alien warning sound
            alarm_s = False
            interval_s = True
            #ct_speed = 30
        
        screen.blit(aquarium1,(0,0)) #top part of the background
        screen.blit(aquarium2,(0,82)) #lower part of the background
        
        player.display_bank(screen,courierFont)
        
        '''
        #Rough boundary Guidelines
        
        #Boundaries for fish
        #horizontal lines
        pygame.draw.line(screen,(0,0,0),(0,90),(780,90))
        pygame.draw.line(screen,(0,0,0),(0,590),(780,590))
        #vertical lines
        pygame.draw.line(screen,(0,0,0),(15,0),(15,657))
        pygame.draw.line(screen,(0,0,0),(775,0),(775,657))
        
        #Clickbox to purchase guppy
        pygame.draw.rect(screen,(255,255,255),(30,10,48,40))
        '''
        
        supply_drop(moneies,moneybag) #money spawns randomly
        
        for fish in fishies: #changes fish coordinates
            fish.movement()
    
        for event in pygame.event.get():
            #pygame.event.set_allowed((QUIT,MOUSEBUTTONUP))
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN: #cheats
                if event.key == pygame.K_PERIOD:
                    player.bank_value += 5000
                elif event.key == pygame.K_UP:
                    ct_speed += 1
                elif event.key== pygame.K_DOWN:
                    ct_speed -= 1
                elif event.key == pygame.K_h:
                    for c in range(100):
                        fishies.add(Fish([guppy1,guppy2],200,200))
            
            #if mouse is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                player.mouse_pos() #only gets mouse position when user clicks
                if player.check_money(moneies): #picks up money
                    playSound(points)
                elif player.new_fish(fishies,[guppy1,guppy2]):
                    playSound(guppyspawn)
                elif player.pause(): #pauses game
                    pygame.mixer.music.pause()
                    t1 = pygame.mixer.music.get_pos()
                    clicked = False
                    while not clicked:
                        for event in pygame.event.get():
                            pygame.event.set_allowed((QUIT,MOUSEBUTTONUP))
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONUP: #unpaues when screen is clicked
                                clicked = True
                                pygame.mixer.music.unpause()
                                t2 = pygame.mixer.music.get_pos()
                                time_paused += (t2 - t1)
                                break
                else:
                    if player.feed(food_storage): #creates food object
                        playSound(drop_food) #if food is created play sound
        
        
        for pellet in food_storage:
            pellet.movement(screen)
            
            for fish in fishies:
                v1 = intersectsX(pellet.x,fish.x,pellet.width,fish.width)
                v2 = intersectsY(pellet.y,fish.y,pellet.height,fish.height)
                if intersects(v1,v2): #checks if food intersects with fish
                    pellet.kill() #removes food
                    player.max_food -= 1 #food dissapears so one more food allowed on screen
                    fish.fed(moneies,moneybag) #creates money bag if fish is full
                    playSound(slurp) #fish makes eating noise
                
                if pellet.ground(): #deletes pellet and returns bool
                    player.max_food -= 1 #one less pellet on screen
    
    
        for fish in fishies:
            if len(food_storage) > 0:
                for pellet in food_storage:
                    if fish.target != None:
                        if not fish.target.alive(): #fish target is gone
                            fish.target = None
                    if fish.target == None: #assigns fihs target if they have none
                        fish.target = pellet
            else:
                fish.target = None
        
        for bag in moneies:
            screen.blit(bag.image,(bag.x,bag.y))
            bag.movement()
        
       
        for fish in fishies:
            screen.blit(fish.current_image,(fish.x,fish.y))
        
        #pygame.draw.rect(screen, (0,0,0), (540,12,50,40),0)
        pygame.display.update()
        clock.tick(ct_speed)   
        
    
    #preparation for battle
    for fish in fishies: #fishies do not want food anymore
        fish.target = None
    playSound(roar) #alien roar
    
    '''Third Part - alien battle one alien'''
    while True:
        
        for alien in aliens:  
            if alien.hp < 1: #alien is dead
                alien.kill()
                alienx = alien.x 
                alieny = alien.y
                playSound(aliendeath)
                #ct_speed = 30
                soundtrack = pygame.mixer.music.load("tank1music.wav") #normal music plays again
                pygame.mixer.music.play()
                for i in range(5):
                    moneies.add(Money(moneybag,alienx+i*5,alieny)) #money spawns from aliens death

        if len(aliens) == 0:
            break
            
        #if alien.check_alive(): #checks if alien is alive
            #problems killing alien
        
        for event in pygame.event.get():
            pygame.event.set_allowed((QUIT,MOUSEBUTTONUP))
            if event.type == pygame.QUIT:
                sys.exit()
            #if mouse is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                player.mouse_pos() #only gets mouse position when user clicks
                for alien in aliens:
                    if player.shoot(alien):
                        shot = True
                        playSound(laser)
                if player.check_money(moneies): #picks up money
                    playSound(points)
                elif player.pause(): #pauses game
                    clicked = False
                    pygame.mixer.music.pause()
                    while not clicked:
                        for event in pygame.event.get():
                            pygame.event.set_allowed((QUIT,MOUSEBUTTONUP))
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONUP: #unpaues when screen is clicked
                                clicked = True
                                pygame.mixer.music.unpause()
                                break
                
        
        for fish in fishies: #changes fish coordinates
            for alien in aliens:
                fish.movement(4)
                v1 = intersectsX(alien.x,fish.x,80,fish.width)
                v2 = intersectsY(alien.y,fish.y,120,fish.height)
                if intersects(v1,v2): #checks if food intersects with fish
                    fish.kill()
                    playSound(chomp)
                    alien.target = None
            
        for pellet in food_storage:
            pellet.y += 2
            if pellet.ground(): #deletes pellet and returns bool
                player.max_food -= 1 #one less pellet on screen
                
        if len(fishies) == 0:
            screen.blit(gameover,(130,120))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.mixer.music.stop()
            break
        
        #sets a target for alien
        for fish in fishies:
            for alien in aliens:
                alien.set_target(fish)
        
        for alien in aliens:
            alien.eat_movement()
        
        screen.blit(aquarium1,(0,0)) #top part of the background
        screen.blit(aquarium2,(0,82)) #lower part of the background
        
        player.display_bank(screen,courierFont)
        
        for alien in aliens:
            screen.blit(alien.current_image,(alien.x,alien.y))
        
        for bag in moneies:
            bag.movement()
            screen.blit(bag.image,(bag.x,bag.y))
       
        for fish in fishies:
            screen.blit(fish.current_image,(fish.x,fish.y))
        
        for pellet in food_storage:
            screen.blit(pellet.image,(pellet.x,pellet.y))
        
        if shot:
            shot = False #resets bool
            screen.blit(crossh,(player.x_mouse -25, player.y_mouse -22)) #displays crosshairs
        
        pygame.display.update()
        clock.tick(ct_speed)
    
    
    '''Fourth part - Accumulating money'''
    while True:
        
        if len(fishies) == 0: #breaks loop bc all fishes are dead
            break
        if player.bank_value > 2401: #spawns aliens when player gets 2401+ dollars
            break
        
        screen.blit(aquarium1,(0,0)) #top part of the background
        screen.blit(aquarium2,(0,82)) #lower part of the background
        screen.blit(egg,(537,13))
        
        player.display_bank(screen,courierFont) #displays bank
        
        supply_drop(moneies,moneybag) #random money drops
        
        for fish in fishies: #changes fish coordinates
            fish.movement(2)
        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PERIOD:
                    player.bank_value += 5000
                elif event.key == pygame.K_UP:
                    ct_speed += 1
                elif event.key== pygame.K_DOWN:
                    ct_speed -= 1
                elif event.key == pygame.K_h:
                    for c in range(100):
                        fishies.add(Fish([guppy1,guppy2],200,200))
            #if mouse is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                player.mouse_pos() #only gets mouse position when user clicks
                if player.egg():
                    screen.blit(winpic,(150,150))
                    pygame.display.update()
                    pygame.mixer.music.stop()
                    for fish in fishies: #resets the game by deleting everything
                        fish.kill()
                    for money in moneies:
                        money.kill()
                    player.bank_value = 450
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONUP: #game restarts if clicked
                                win = True #loops break and restart
                                break
                        if win:
                            break
                if player.check_money(moneies): #picks up money
                    playSound(points)
                elif player.new_fish(fishies,[guppy1,guppy2]):
                    playSound(guppyspawn)
                elif player.pause(): #pauses game
                    clicked = False
                    pygame.mixer.music.pause()
                    while not clicked:
                        for event in pygame.event.get():
                            pygame.event.set_allowed((QUIT,MOUSEBUTTONUP))
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONUP: #unpaues when screen is clicked
                                clicked = True
                                pygame.mixer.music.unpause()
                                break
                else:
                    if player.feed(food_storage): #creates food object
                        playSound(drop_food) #if food is created play sound
        
        if win:
            break
        
        
        for pellet in food_storage:
            pellet.movement(screen)
            
            for fish in fishies:
                v1 = intersectsX(pellet.x,fish.x,pellet.width,fish.width)
                v2 = intersectsY(pellet.y,fish.y,pellet.height,fish.height)
                if intersects(v1,v2): #checks if food intersects with fish
                    pellet.kill() #removes food
                    player.max_food -= 1 #food dissapears so one more food allowed on screen
                    fish.fed(moneies,moneybag) #creates money bag if fish is full
                    playSound(slurp) #fish makes eating noise
                
                if pellet.ground(): #deletes pellet and returns bool
                    player.max_food -= 1 #one less pellet on screen
    
    
        for fish in fishies:
            if len(food_storage) > 0:
                for pellet in food_storage:
                    if fish.target != None:
                        if not fish.target.alive(): #fish target is gone
                            fish.target = None
                    if fish.target == None: #assigns fihs target if they have none
                        fish.target = pellet
            else:
                fish.target = None #when theres no food
        
        for bag in moneies:
            screen.blit(bag.image,(bag.x,bag.y))
            bag.movement()
        
       
        for fish in fishies:
            screen.blit(fish.current_image,(fish.x,fish.y))
        
        pygame.display.update()
        clock.tick(ct_speed)
    #preparation for battle
    for fish in fishies: #fishies do not want food anymore
        fish.target = None
        
    playSound(roar) #alien roar
    aliens.add(Alien([alien1,alien2], 50, 200))
    aliens.add(Alien([alien1,alien2], 300, 200))
    pygame.mixer.music.load("alienbattle.wav") #loads music for battle
    pygame.mixer.music.play(5) #plays music for battle, loops 5 times
    #alien battle with two aliens
    
    
    '''Fifth Part - Alien battle Two aliens'''
    while True:
        
        
        for alien in aliens:  
            if alien.hp < 1: #alien is dead
                alien.kill()
                alienx = alien.x 
                alieny = alien.y
                playSound(aliendeath)
                #ct_speed = 30
                for i in range(5):
                    moneies.add(Money(moneybag,alienx+i*5,alieny)) #money spawns from aliens death

        if len(aliens) == 0: #all aliens are dead
            break
            
        for event in pygame.event.get():
            pygame.event.set_allowed((QUIT,MOUSEBUTTONUP))
            if event.type == pygame.QUIT:
                sys.exit()
            #if mouse is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                player.mouse_pos() #only gets mouse position when user clicks
                for alien in aliens:
                    if player.shoot(alien):
                        shot = True
                        playSound(laser)
                if player.check_money(moneies): #picks up money
                    playSound(points)
                elif player.pause(): #pauses game
                    clicked = False
                    pygame.mixer.music.pause()
                    while not clicked:
                        for event in pygame.event.get():
                            pygame.event.set_allowed((QUIT,MOUSEBUTTONUP))
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONUP: #unpaues when screen is clicked
                                clicked = True
                                pygame.mixer.music.unpause()
                                break
                
        
        for fish in fishies: #changes fish coordinates
            for alien in aliens:
                fish.movement(4)
                v1 = intersectsX(alien.x,fish.x,80,fish.width)
                v2 = intersectsY(alien.y,fish.y,120,fish.height)
                if intersects(v1,v2): #checks if food intersects with fish
                    fish.kill()
                    playSound(chomp)
                    alien.target = None
                if alien.target != None:
                    if not alien.target.alive(): #aliens target is no longer alive
                        alien.target = None
            
        for pellet in food_storage:
            pellet.y += 2
            if pellet.ground(): #deletes pellet and returns bool
                player.max_food -= 1 #one less pellet on screen
                
        if len(fishies) == 0:
            screen.blit(gameover,(130,120))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.mixer.music.stop()
            break
        
        #sets a target for alien
        for fish in fishies:
            for alien in aliens:
                alien.set_target(fish)
        
        for alien in aliens:
            alien.eat_movement()
        
        screen.blit(aquarium1,(0,0)) #top part of the background
        screen.blit(aquarium2,(0,82)) #lower part of the background
        
        player.display_bank(screen,courierFont)
        
        for alien in aliens:
            screen.blit(alien.current_image,(alien.x,alien.y))
        
        for bag in moneies:
            bag.movement()
            screen.blit(bag.image,(bag.x,bag.y))
       
        for fish in fishies:
            screen.blit(fish.current_image,(fish.x,fish.y))
        
        for pellet in food_storage:
            screen.blit(pellet.image,(pellet.x,pellet.y))
        
        if shot:
            shot = False
            screen.blit(crossh,(player.x_mouse -25, player.y_mouse -22))
        
        pygame.display.update()
        clock.tick(ct_speed)
    
    soundtrack = pygame.mixer.music.load("tank1music.wav")
    pygame.mixer.music.play(3)  #song loops 3 times

    '''Final Part - Achieving Victory'''
    while True:
        
        if len(fishies) == 0: #breaks loop bc all fishes are dead
            break
        
        screen.blit(aquarium1,(0,0)) #top part of the background
        screen.blit(aquarium2,(0,82)) #lower part of the background
        screen.blit(egg,(537,13))
        
        player.display_bank(screen,courierFont) #displays bank
        
        supply_drop(moneies,moneybag) #random money drops
        
        for fish in fishies: #changes fish coordinates
            fish.movement(2)
        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PERIOD:
                    player.bank_value += 5000
                elif event.key == pygame.K_UP:
                    ct_speed += 1
                elif event.key== pygame.K_DOWN:
                    ct_speed -= 1
                elif event.key == pygame.K_h:
                    for c in range(100):
                        fishies.add(Fish([guppy1,guppy2],200,200))
            #if mouse is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                player.mouse_pos() #only gets mouse position when user clicks
                if player.egg():
                    screen.blit(winpic,(150,150))
                    pygame.display.update()
                    pygame.mixer.music.stop()
                    playSound(applause)
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONUP: #game restarts if clicked
                                win = True #loops break and restart
                                break
                        if win:
                            break
                if player.check_money(moneies): #picks up money
                    playSound(points)
                elif player.new_fish(fishies,[guppy1,guppy2]):
                    playSound(guppyspawn)
                elif player.pause(): #pauses game
                    clicked = False
                    pygame.mixer.music.pause()
                    while not clicked:
                        for event in pygame.event.get():
                            pygame.event.set_allowed((QUIT,MOUSEBUTTONUP))
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONUP: #unpaues when screen is clicked
                                clicked = True
                                pygame.mixer.music.unpause()
                                break
                else:
                    if player.feed(food_storage): #creates food object
                        playSound(drop_food) #if food is created play sound
        
        if win:
            playSound(click)
            break
        
        
        for pellet in food_storage:
            pellet.movement(screen)
            
            for fish in fishies:
                v1 = intersectsX(pellet.x,fish.x,pellet.width,fish.width)
                v2 = intersectsY(pellet.y,fish.y,pellet.height,fish.height)
                if intersects(v1,v2): #checks if food intersects with fish
                    pellet.kill() #removes food
                    player.max_food -= 1 #food dissapears so one more food allowed on screen
                    fish.fed(moneies,moneybag) #creates money bag if fish is full
                    playSound(slurp) #fish makes eating noise
                
                if pellet.ground(): #deletes pellet and returns bool
                    player.max_food -= 1 #one less pellet on screen
    
    
        for fish in fishies:
            if len(food_storage) > 0:
                for pellet in food_storage:
                    if fish.target != None:
                        if not fish.target.alive(): #fish target is gone
                            fish.target = None
                    if fish.target == None: #assigns fihs target if they have none
                        fish.target = pellet
            else:
                fish.target = None #when theres no food
        
        for bag in moneies:
            screen.blit(bag.image,(bag.x,bag.y))
            bag.movement()
        
       
        for fish in fishies:
            screen.blit(fish.current_image,(fish.x,fish.y))
        
        pygame.display.update()
        clock.tick(ct_speed)
    for alien in aliens:
        alien.kill()
    for fish in fishies: #resets the game by deleting everything
        fish.kill()
    for money in moneies:
        money.kill()
    player.bank_value = 500