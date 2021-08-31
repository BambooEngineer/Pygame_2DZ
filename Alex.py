import pygame 
import random
import math
import time
pygame.init()
random.seed()       # Analyze Code

# change from wave survival to open world survival:     Jumping is supposed to be hard, zombies are supposed to be hard to get passed, this is why you need to scavenge to fight
    
    # more loot, buildings with open and closable doors, grow food
    # LAN muiltiplayer
   

GameStart = pygame.mixer.Sound("Funny.wav")
GunShot = pygame.mixer.Sound("Gun1.wav")
ZombiesYell = pygame.mixer.Sound("Yell(1).wav")
ZombieScream = pygame.mixer.Sound("Group(1).wav")
BlockTearDown = pygame.mixer.Sound("TearDown.wav") # Add to Block Class


black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((800,600)) # resolution, xy
pygame.display.set_caption('2DZ')
clock = pygame.time.Clock()
clock.tick(60)

bg = pygame.image.load('City.jpg') 
bg2 = pygame.image.load('City.jpg')
bg1 = pygame.image.load('City.jpg')


class player:

    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
    AmmoImg = pygame.image.load('Bullets.png')
    
    AxeHR = pygame.image.load('BatHoldL.png')
    AxeHL = pygame.image.load('BatHoldR.png')
    AxeR = pygame.image.load('BatWackL.png')
    AxeL = pygame.image.load('BatWackR.png')

    
    
    left = False
    right = False
    walkCount = 0 
    direction = True
    Ammo = 10
    ball_changex = 0
    ball_changey = 0
    ballx = 400
    bally = 500

    Stamina = 10

    jump = 0
    air = False
    up = False
    fall = False

    Wood = 0

    def __init__(self):
        pass

    #@staticmethod
    def redrawPlayer(self, x, y): 
    
        
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if self.left:  # If we are facing left
            gameDisplay.blit(self.walkLeft[self.walkCount//3], (x,y))  
            self.walkCount += 1        
            self.direction = False
        if self.right:
            gameDisplay.blit(self.walkRight[self.walkCount//3], (x,y))
            self.walkCount += 1
            self.direction = True
        else:
            
            if self.direction: 
                gameDisplay.blit(self.walkRight[0], (x,y))
            if not(self.direction) and not(self.left):
                gameDisplay.blit(self.walkLeft[0], (x,y))

     
        if self.air: # True          
            if self.up: # No Velocity/Collisions here, Just simple y Movement
                if self.bally >= 450: # if not jumping
                    self.jump -= 1 # jump
                else:
                    self.fall = True
                    self.up = False
            if self.fall:
                if not(self.bally >= 500): # if not on ground
                    self.jump += 1 # fly down           # On top of block
                else:
                    self.jump = 0
                    self.bally = 500
                    self.fall = False
                    self.air = False

    @staticmethod
    def redrawGameWindow(x, y): 
    
        
        if player.walkCount + 1 >= 27:
            player.walkCount = 0
        
        if player.left:  # If we are facing left
            gameDisplay.blit(player.walkLeft[player.walkCount//3], (x,y))  
            player.walkCount += 1                           
            player.direction = False
        if player.right:
            gameDisplay.blit(player.walkRight[player.walkCount//3], (x,y))
            player.walkCount += 1
            player.direction = True
        else:
            
            if player.direction: 
                gameDisplay.blit(player.walkRight[0], (x,y)) 
            if not(player.direction) and not(player.left):
                gameDisplay.blit(player.walkLeft[0], (x,y))

    def Shotgun(self, x,y): 
        if self.direction: # imaged ontop of player pixels
            gameDisplay.blit(ShogunL, (x,y)) 
        if not(self.direction):
            gameDisplay.blit(ShogunR, (x,y))

    def AxeH(self, x,y): # axehold
        if self.direction: 
            gameDisplay.blit(self.AxeHL, (x+7,y+5)) 
        if not(self.direction): # right
            gameDisplay.blit(self.AxeHR, (x-18,y+5))
    def AxeW(self, x,y): # axewack
        if self.direction: 
            gameDisplay.blit(self.AxeL, (x+10,y)) 
        if not(self.direction): # right
            gameDisplay.blit(self.AxeR, (x-10,y))
            
    def HoldB(self): # hold block
        if self.direction: 
            gameDisplay.blit(BLOCKS.BlockSelect, (self.ballx+50, self.bally+40))
        if not(self.direction): 
            gameDisplay.blit(BLOCKS.BlockSelect, (self.ballx-15, self.bally+40))

#################
class Tree:

    Tree1 = pygame.image.load('Tree1.png')
    Tree2 = pygame.image.load('Tree2.png')
    Tree3 = pygame.image.load('Tree3.png') 
    Tree4 = pygame.image.load('Tree4.png')

    Pick = [Tree1,Tree2,Tree3,Tree4] # random.randint(0,3)

    @staticmethod
    def TreeSpawn(x, select, y=415):
        gameDisplay.blit(Tree.Pick[select], (x,y))

class Energy:

    Drink = pygame.image.load('Drink.png')

    @staticmethod
    def DrinkSpawn(x, y=480): 
        gameDisplay.blit(Energy.Drink, (x,y))
        


class BLOCKS: # Blocks made from Wood Mined from Trees
    # Wood Amount from trees vary ADD
    Block = pygame.image.load('Block.png')
    BlockSelect = pygame.image.load('BlockSelect.png')
    Blockx = [] 
    Blocky = []
    Health = []
    Blocks = 0
    BlockPlaced = False
        
    boxL = False # HitBoxes
    boxR = False 
#######################

class Helicopter:
    Stop = False
    Call = False
    #global ballx = 0
    #global bally = 0
    ladder = pygame.image.load('ladder.jpg')
    Heli = pygame.image.load('Heli.jpg')
    
    
    def __init__(self):
        
        helix = -300 # left to right
        heliy = 50
        gameDisplay.blit(bg, (bgX, 0)) # background
        gameDisplay.blit(bg2, (bgX2, 0))
        for x in range(helix, 900):
            if(x >= 450 and not(Helicopter.Stop)): # Stops it then keeps moving
                for y in range(50, 490): # drop him
                    player.redrawGameWindow(x, y) # at x 
                    gameDisplay.blit(Helicopter.Heli, (x,heliy)) # keep heli in air
                    pygame.display.update()
                    gameDisplay.blit(bg, (bgX, 0)) # background
                Helicopter.Stop = True # heli flys away
            gameDisplay.blit(Helicopter.Heli, (x,heliy))
            pygame.display.update()
            

    @classmethod
    def heliPick(cls):
        
        helix = 900 # right to left
        heliy = 50
        gameDisplay.blit(bg, (bgX, 0)) # background
        for x in range(450, 900):
            helix = helix - 1
            gameDisplay.blit(Helicopter.Heli, (helix,heliy))
            pygame.display.update()

    @classmethod
    def heliLeave(cls):
        
        helix = 450 # right to left
        heliy = 50
        for x in range(-300, helix):
            helix = helix - 1
            gameDisplay.blit(Helicopter.Heli, (helix,heliy))
            pygame.display.update()
        pygame.quit()
        quit()

    @staticmethod
    def LadderGrab(Hx, Hy, Lx, Ly):
        
         # Heli Pick up collision
        if(True):
            gameDisplay.blit(Helicopter.Heli, (Hx,Hy)) # Enable Heli to Stay
            areaR = math.hypot(Lx - player.ballx,460-player.bally) # after calling heli jump in
            gameDisplay.blit(Helicopter.ladder, (Lx,Ly))
            
            if(areaR <= 50):
                Helicopter.heliLeave()   


class Zombie:

    Baby = [pygame.image.load('Ground.png'), pygame.image.load('Climb.png'), pygame.image.load('Fist.png'), pygame.image.load('Hand.png'), pygame.image.load('Baldy.png'), pygame.image.load('Head.png'), pygame.image.load('Lower_Body.png'), pygame.image.load('Body.png'), pygame.image.load('Zombie.png')]
    ZHeadless = [pygame.image.load('RightHeadless.png'), pygame.image.load('LeftHeadless.png')]
    ZHead = [pygame.image.load('LeftHead.png'),pygame.image.load('RightHead.png')]
# Baby = Spawn Animation, Headless = 3 Shots, Head = 5 Shots, Crawlers get jumped on
    ZCrawlerRight = [pygame.image.load('CrawlerRight.png'),pygame.image.load('CrawlerRight1.png'), pygame.image.load('CrawlerRight2.png')]
    ZCrawlerLeft = [pygame.image.load('CrawlerLeft.png'), pygame.image.load('CrawlerLeft1.png'), pygame.image.load('CrawlerLeft2.png')]
    DamageR = pygame.image.load('ShotR.png')
    DamageL = pygame.image.load('ShotL.png')

    HunteR = [pygame.image.load('HunterMR8.png'), pygame.image.load('HunterMR7.png'), pygame.image.load('HunterMR6.png'), pygame.image.load('HunterMR5.png'), pygame.image.load('HunterMR4.5.png'), pygame.image.load('HunterMR4.png'), pygame.image.load('HunterMR3.png'), pygame.image.load('HunterMR2.png'), pygame.image.load('HunterMR1.png')]
    HunteL = [pygame.image.load('HunterML8.png'), pygame.image.load('HunterML7.png'), pygame.image.load('HunterML6.png'), pygame.image.load('HunterML5.png'), pygame.image.load('HunterML4.5.png'), pygame.image.load('HunterML4.png'), pygame.image.load('HunterML3.png'), pygame.image.load('HunterML2.png'), pygame.image.load('HunterML1.png')]

    
    SpawnCount = 0
    
    CrawlerCount = []
    Hunter = []         # Hunter Z instead of Crawl Variable
    cleft = [] # maybe
    cright = []
    NoBlockR = []
    NoBlockL = []
    crawl_changex = [] # changes
    crawl_changey = 0
    crawlx = [] # changes
    crawly = 500 # Hunter Zs have modified y in statements


    
    Health = [] # changes
    ZNum = 0 # keep amount in check
    

    
    def __init__(self, X, CorH): # CorH can be an array with random inside parameter
        Zombie.ZNum += 1 # Adds another Zombie along
        if CorH:
            pygame.mixer.Sound.play(ZombiesYell)
            Zombie.Hunter.append(True)
        else:
            Zombie.Hunter.append(False)
        Zombie.Health.append(5) # with adding all of its default values
        Zombie.cleft.append(False) 
        Zombie.cright.append(False)
        Zombie.NoBlockR.append(False)
        Zombie.NoBlockL.append(False)
        Zombie.crawlx.append(X)
        Zombie.crawl_changex.append(0)
        Zombie.CrawlerCount.append(0)
        
        #pass
        
        gameDisplay.blit(bg1, (bgX1, 0)) 
        gameDisplay.blit(bg, (bgX, 0))
        gameDisplay.blit(bg2, (bgX2, 0))
        if Zombie.ZNum < 2: 
            if Zombie.SpawnCount + 1 >= 135: # 9 images * 15 = 135 
                Zombie.SpawnCount = 0 # how many times an image gets displayed 

            for x in range(0,135): 
                gameDisplay.blit(bg1, (bgX1, 0)) # settled with interrupt
                gameDisplay.blit(bg, (bgX, 0))
                gameDisplay.blit(bg2, (bgX2, 0))
                player.redrawGameWindow(player.ballx, player.bally)
                gameDisplay.blit(Zombie.Baby[Zombie.SpawnCount//15], (X,500))  # We integer divide walkCounr by 3 to ensure each
                pygame.display.update()
                Zombie.SpawnCount += 1

    def Reanimate(X, CorH, i): # instead of adding data to lists just modify existing so amount of data corresponds to amount of living Zombies
        Zombie.ZNum += 1 
        if CorH: # if hunter 
            #pygame.mixer.Sound.play(ZombiesYell) # respawn
            Zombie.Hunter[i] = True
        else:
            Zombie.Hunter[i] = False
        #Zombie.cleft[i]= 
        #Zombie.cright[i]=
        #Zombie.NoBlockR[i]=
        #Zombie.NoBlockL[i]=
        Zombie.crawlx[i]= X
        #Zombie.crawl_changex[i]=
        #Zombie.CrawlerCount[i] =
        

    #@classmethod @staticmethod
    def Crawlers(i):                            # animations
        if not(Zombie.Hunter[i]):
            if Zombie.CrawlerCount[i] + 1 >= 15: # this controls how many times a image is shown
                Zombie.CrawlerCount[i] = 0 # >= x must be a 3rd multiple of the //x
                # Zombie. if self doesnt work ( trying individuals ) 
            if Zombie.cleft[i]:  # If we are facing left
                gameDisplay.blit(Zombie.ZCrawlerLeft[Zombie.CrawlerCount[i]//5], (Zombie.crawlx[i],500))  # We integer divide walkCounr by 3 to ensure each
                Zombie.CrawlerCount[i] += 1                           # image is shown 3 times every animation
            elif Zombie.cright[i]:
                gameDisplay.blit(Zombie.ZCrawlerRight[Zombie.CrawlerCount[i]//5], (Zombie.crawlx[i],500))
                Zombie.CrawlerCount[i] += 1
        else:
            if Zombie.CrawlerCount[i] + 1 >= 27: 
                Zombie.CrawlerCount[i] = 0 
                
            if Zombie.cleft[i]:  
                gameDisplay.blit(Zombie.HunteL[Zombie.CrawlerCount[i]//3], (Zombie.crawlx[i],445))  
                Zombie.CrawlerCount[i] += 1                           
            elif Zombie.cright[i]:
                gameDisplay.blit(Zombie.HunteR[Zombie.CrawlerCount[i]//3], (Zombie.crawlx[i],445))
                Zombie.CrawlerCount[i] += 1
            

    def LetLoose(i,x):                              # Movement
            if Zombie.Health[i] > 0:
                Zombie.Crawlers(i) # animation initializers
            if not(Zombie.Hunter[i]):
                if(Zombie.crawlx[i] >= x): # Crawler Movement
                    if not(Z.NoBlockL[i]):
                        Zombie.crawlx[i] -= 1  #( follow player )
                        Zombie.cleft[i] = True # Animation Settings
                        Zombie.cright[i] = False
                if(Zombie.crawlx[i] <= x):
                    if not(Z.NoBlockR[i]):
                        Zombie.crawlx[i] += 1
                        Zombie.cleft[i] = False
                        Zombie.cright[i] = True
            else:
                if(Zombie.crawlx[i]+88 >= x and x >= Zombie.crawlx[i]+88 - 300): # hunter Movement, update: hunters will not chase unless approached, this makes the game less 'wave' like and more survival
                    if not(Z.NoBlockL[i]):  # hunter wake up is determined by player falling into a certain area behind or infront of it
                        Zombie.crawlx[i] -= 3  
                        Zombie.cleft[i] = True 
                        Zombie.cright[i] = False
                if(Zombie.crawlx[i]+88 <= x and x <= Zombie.crawlx[i] + 300): # x[i]+88 is to compensate for the image offset of the hunters
                    if not(Z.NoBlockR[i]):
                        Zombie.crawlx[i] += 3
                        Zombie.cleft[i] = False
                        Zombie.cright[i] = True
                
        


    
HoldGunL = pygame.image.load('S_GunLeft.png')
HoldGunR = pygame.image.load('S_GunRight.png')
ShogunL = pygame.image.load('ShotgunLeft.png')
ShogunR = pygame.image.load('ShotgunRight.png')
GunL = False

def things(thingx, thingy, radiusw, color):
    pygame.draw.circle(gameDisplay,color,[thingx,thingy],(radiusw))

def Ammo(x,y):
    gameDisplay.blit(player.AmmoImg, (x,y))


pygame.joystick.init()
joysticks = pygame.joystick.Joystick(0)
joysticks.init()

crashed = False
###########################################
bgX1_change = 0
bgX_change = 0
bgX2_change = 0

bgX1 = bg.get_width() * -1 # -1280
bgX = 0
bgX2 = bg.get_width() # 1280
############################################
AxeAttack = False

gunSpawn = random.randint(5, 710) # spawns once
AmmoSpawn = random.randint(-1200, 1200)
AmmoE = True 
Grab = True
Pickup = False
Weapon = False
bullet_changex = 0
bulletx = player.ballx+10
shoot = False
bulletfly = False
# from 5 to 710 for x at 500 y
# maybe reoptimize if guns and Z types get added = 2 players last
inventory = 2 # 3 = bat, gun, blocks(future update = types & basebuilding)
increment = 0
score = 0

Treex = random.randint(-1000,1000)
Drinkx = random.randint(-1000,1000)
TreeS = random.randint(0,2)


pygame.mixer.Sound.play(GameStart)
#H = Helicopter() # HELI CLASS
#pygame.mixer.Sound.play(ZombiesYell) # Hunter yell with new Z
pygame.mixer.Sound.play(ZombieScream) # Group Yell every few score

LeftorRightZ = [True, False]
if LeftorRightZ[random.randint(0,1)]: #SPAWN
    Z = Zombie(random.randint(player.ballx-2000,player.ballx-1000),False) 
    Z = Zombie(random.randint(player.ballx-2000,player.ballx-1000),False) 
    Z = Zombie(random.randint(player.ballx-2000,player.ballx-1000),False) 
else:
    Z = Zombie(random.randint(player.ballx+1000,player.ballx+2000),False) 
    Z = Zombie(random.randint(player.ballx+1000,player.ballx+2000),False) 
    Z = Zombie(random.randint(player.ballx+1000,player.ballx+2000),False)


P = player()

#print("U Gotta Z Job")

tree_changex = 0
drink_changex = 0
block_changex = 0
ammo_change = 0
gun_change = 0
Z_change = 0
Drink_change = 0

areaBL = 0
areaBR = 0
areaZL = 0
areaZR = 0
Cancel = False

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text, text2, text3):
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextSurf1, TextRect1 = text_objects(text2, largeText)
    TextSurf2, TextRect2 = text_objects(text3, largeText)
    TextRect.center = ((100),(100))
    TextRect1.center = ((100),(130))
    TextRect2.center = ((100),(160))
    gameDisplay.blit(TextSurf, TextRect)
    gameDisplay.blit(TextSurf1, TextRect1)
    gameDisplay.blit(TextSurf2, TextRect2)

font = pygame.font.Font('freesansbold.ttf',50)

while not crashed:          
    gameDisplay.blit(bg1, (bgX1, 0)) # Backgrounds
    gameDisplay.blit(bg, (bgX, 0))
    gameDisplay.blit(bg2, (bgX2, 0)) # its at the end of original img
    
    message_display("Ammo: "+str(P.Ammo), "Stamina "+str(P.Stamina), "Wood: "+str(P.Wood)) # Display Player Values
   
    
    hats = joysticks.get_numhats()

    

    for i in range(hats):                   # DPAD CONTROLS WITH SCREEN SHIFTING
            hat = joysticks.get_hat(i)
            #print("{}: {}".format(i, str(hat)))
            Dpad = str(hat)
            #print(Dpad) # returns (x, y) based on dpad buttons
            if Dpad == "(1, 0)": # Right
                bgX1_change = -3
                bgX_change = -3 # scroll left
                bgX2_change = -3
                tree_changex = -3
                drink_changex = -3
                P.left = False
                P.right = True
                block_changex = -3 # each value inside
                ammo_change = -3
                gun_change = -3
                Z_change = -3
                
                    
               

            if Dpad == "(-1, 0)": # Left
                bgX1_change = 3
                bgX_change = 3 # scroll right
                bgX2_change = 3
                tree_changex = 3
                drink_changex = 3
                P.left = True
                P.right = False
                block_changex = 3 # each value inside
                ammo_change = 3
                gun_change = 3
                Z_change = 3
                
                    
        

            if Dpad == "(0, 1)": # Jump
                if P.bally >= 450: 
                    P.air = True
                    P.up = True
                if(P.bally >= 520):
                    P.bally = 520
                    

            if Dpad == "(1, 1)": # JRight -1.4
                if P.bally >= 450: 
                    P.air = True
                    P.up = True
                bgX1_change = -1.4
                bgX_change = -1.4 # scroll left
                bgX2_change = -1.4
                tree_changex = -1.4
                drink_changex = -1.4
                block_changex = -1.4
                P.left = False
                P.right = True
                ammo_change = -1.4
                gun_change = -1.4
                Z_change = -1.4
                if(P.bally >= 520):
                    P.bally = 520

            if Dpad == "(-1, 1)": # JLeft
                if P.bally >= 450: 
                    P.air = True
                    P.up = True
                bgX1_change = 1.4
                bgX_change = 1.4 # scroll right
                bgX2_change = 1.4 
                tree_changex = 1.4
                drink_changex = 1.4
                block_changex = 1.4 # each value inside
                P.left = True
                P.right = False
                ammo_change = 1.4
                gun_change = 1.4
                Z_change = 1.4
                if(P.bally >= 520):
                    P.bally = 520
                

            if Dpad == "(0, -1)": # down inventory control
                increment += 1 

            if Dpad == "(0, 0)": # Default
                bgX1_change = 0
                bgX_change = 0
                bgX2_change = 0
                tree_changex = 0
                drink_changex = 0
                block_changex = 0
                ammo_change = 0
                gun_change = 0
                Z_change = 0
                P.left = False
                P.right = False
                
    for event in pygame.event.get(): # print events by how many times it occurs 
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.JOYBUTTONDOWN: # ACTION BUTTON
            bulletx = P.ballx+10
            BLOCKS.BlockPlaced = True 
            if inventory == 1: # Gun
                shoot = True
            if inventory == 2: # Axe
                AxeAttack = True
            if inventory == 0: # Block Placing
                if BLOCKS.BlockPlaced and P.Wood >= 1:
                    LeftorRightZ = [True, False]
                    if LeftorRightZ[random.randint(0,1)]: #SPAWN
                        Z = Zombie(random.randint(player.ballx-2000,player.ballx-1000),False)  
                    else:
                        Z = Zombie(random.randint(player.ballx+1000,player.ballx+2000),False)
                    if P.direction:
                        BLOCKS.Blocks += 1 
                        P.Wood -= 1
                        BLOCKS.Blockx.append(P.ballx+50)
                        BLOCKS.Blocky.append(P.bally+40)
                        BLOCKS.Health.append(15)
                        BLOCKS.BlockPlaced = False
                    if not(P.direction): 
                        BLOCKS.Blocks += 1
                        P.Wood -= 1
                        BLOCKS.Blockx.append(P.ballx-15)
                        BLOCKS.Blocky.append(P.bally+40)
                        BLOCKS.Health.append(15)
                        BLOCKS.BlockPlaced = False
            

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
            
    # Animations
    
    if increment > 30: # inventory selection
        inventory = 0
    if increment > 40:
        increment = 0
    if increment < 10 and increment > 0:
        inventory = 2
    if increment > 20 and increment < 30:
        inventory = 1

    for i in range(Zombie.ZNum): # Reset Direction Enablers after canceled for block collision
        Zombie.NoBlockL[i] = False 
        Zombie.NoBlockR[i] = False
        
    for i in range(BLOCKS.Blocks): # Positioning WORKS
        areaBL = math.hypot(BLOCKS.Blockx[i]-P.ballx, BLOCKS.Blocky[i]-P.bally-20)
        areaBR = math.hypot(BLOCKS.Blockx[i]-20-P.ballx, BLOCKS.Blocky[i]-P.bally-20)

        for x in range(Zombie.ZNum):
            if Zombie.Hunter[x]:
                areaZL = math.hypot(Zombie.crawlx[x]+88-BLOCKS.Blockx[i], BLOCKS.Blocky[i]-Zombie.crawly-20)
                areaZR = math.hypot(Zombie.crawlx[x]+88+40-BLOCKS.Blockx[i], BLOCKS.Blocky[i]-Zombie.crawly-20)
                if Zombie.cleft[x] and areaZL <= 22:
                    Zombie.NoBlockL[x] = True # Just cant go that direction 
                    Zombie.NoBlockR[x] = False
                    pygame.mixer.Sound.play(BlockTearDown)
                    BLOCKS.Health[i] -= 1 # TearDown
                if Zombie.cright[x] and areaZR <= 22:
                    Zombie.NoBlockL[x] = False
                    Zombie.NoBlockR[x] = True
                    pygame.mixer.Sound.play(BlockTearDown)
                    BLOCKS.Health[i] -= 1 # TearDown
            else:
                areaZL = math.hypot(Zombie.crawlx[x]-BLOCKS.Blockx[i], BLOCKS.Blocky[i]-Zombie.crawly-20)
                areaZR = math.hypot(Zombie.crawlx[x]+40-BLOCKS.Blockx[i], BLOCKS.Blocky[i]-Zombie.crawly-20)
                if Zombie.cleft[x] and areaZL <= 22:
                    Zombie.NoBlockL[x] = True # Just cant go that direction 
                    Zombie.NoBlockR[x] = False
                if Zombie.cright[x] and areaZR <= 22:
                    Zombie.NoBlockL[x] = False
                    Zombie.NoBlockR[x] = True
        
        if areaBL <= 22 and P.left: # left
                bgX1_change = 0 # 
                bgX_change = 0 # 
                bgX2_change = 0 # 
                tree_changex = 0
                drink_changex = 0
                block_changex = 0
                ammo_change = 0
                gun_change = 0
                Z_change = 0
                
                
        if ((areaBL <= 35 or areaBR <= 35) and P.fall): # jumping on
            P.jump = 0
            P.fall = False
            P.bally = BLOCKS.Blocky[i]-50 
            Cancel = True # Fall down 
        if Cancel: # Falling Off 
            if ((areaBL > 30 or areaBR > 35) and P.bally <= 500):
                P.air = True
                P.up = False
                P.fall = True
                if P.bally == 500:
                    Cancel = False
        if areaBR <= 30 and P.right: # right
                bgX1_change = 0 # 
                bgX_change = 0
                bgX2_change = 0
                tree_changex = 0
                drink_changex = 0
                block_changex = 0
                ammo_change = 0
                gun_change = 0
                Z_change = 0
                
                

                
    AmmoSpawn += ammo_change 
    gunSpawn += gun_change 
    for i in range(Zombie.ZNum):
        Zombie.crawlx[i] += Z_change      
    P.bally += P.jump # Jump init
    Treex += tree_changex
    Drinkx += drink_changex 
    P.ballx += P.ball_changex

    for i in range(BLOCKS.Blocks): # Positioning WORKS
        BLOCKS.Blockx[i] += block_changex

    
    bulletx += bullet_changex   
    areaGun = math.hypot(gunSpawn - P.ballx,520-P.bally) # pick up collision
    areaAmmo = math.hypot(AmmoSpawn - P.ballx, 520-P.bally)
    areaTree = math.hypot(Treex - P.ballx, 515-P.bally)
    areaDrink = math.hypot(Drinkx - P.ballx, 515-P.bally)
###################################################Gun Mechanics
    if Grab:
        P.Shotgun(gunSpawn, 520)# Spawn Gun
    if(areaGun <= 30): # Gun Pickup
        #print("Pickup")
        if Grab: # Switch from Grab to Hold
            Pickup = True
            Grab = False
    if AmmoE:  # Ammo Pickup
        Ammo(AmmoSpawn,520) 
        if(areaAmmo <= 30): 
        #print("Pickup")
            if Weapon and P.Ammo == 0: 
                P.Ammo = 8 # add Ammo
                LeftorRightZ = [True, False]
                if score < 15:
                    if LeftorRightZ[random.randint(0,1)]: #SPAWN
                        AmmoSpawn = P.ballx-400 # new Spawn
                    else:
                        AmmoSpawn = P.ballx+400 # new Spawn
                if score > 15:
                    P.Ammo = 10
                    if LeftorRightZ[random.randint(0,1)]: #SPAWN
                        AmmoSpawn = P.ballx-200 # new Spawn
                    else:
                        AmmoSpawn = P.ballx+200 # new Spawn
                AmmoE = False # No more pick up at this spawn
    if Pickup and inventory == 1: 
        P.Shotgun(P.ballx, P.bally+10) # Hold
        Weapon = True
    if Weapon:
        if shoot:
            if P.Ammo > 0:
                pygame.mixer.Sound.play(GunShot)
                P.Ammo -= 1 
                bulletfly = True
            shoot = False
    #print(Zombie.ZNum) number stays 
    #print(Zombie.Health) data doesnt 
######################################### Zombie Crawler Spawn & Health
    for i in range(Zombie.ZNum):
        if Zombie.Health[i] > 0: # if still alive
            if Zombie.Hunter[i]:
                areaZ = math.hypot((Zombie.crawlx[i]+88) - P.ballx,Zombie.crawly-P.bally) # Zombie collision
                areaBullet = math.hypot(bulletx - (Zombie.crawlx[i]+88),P.bally-P.bally) # Bullet
            else:
                areaZ = math.hypot(Zombie.crawlx[i] - P.ballx,Zombie.crawly-P.bally) # Zombie collision
                areaBullet = math.hypot(bulletx - Zombie.crawlx[i],P.bally-P.bally) # Bullet
            if(areaZ <= 20): # Crawler Bite
                print("You Got Bit")
                time.sleep(1)
                crashed = True
                #quit()
            Zombie.LetLoose(i,P.ballx) # the incrementing i in the loop is a function parameter so theres not another loop inside the function
        if Zombie.Health[i] == 0: 
            #H.heliPick() # call helicopter
            #Helicopter.Call = True # with heliPick
            Zombie.ZNum -= 1
            score += 1
            print("Score: "+str(score))
            AmmoE = True
            LeftorRightZ = [True, False] # Managing the amount of zombies alive = New Zombie Spawn- New Data Added to all lists + Zombie Amount increases hence increase number of times Zombie Loops occur
            if score < 15:              # Zombie dies, which requires another one to spawn but keep the number of times a zombie loop occurs centered around how many are actually up and moving 
                if LeftorRightZ[random.randint(0,1)]: # So Zombie.Reanimate brings one back which increases the ZNum amount after it decreases by 1, 
                    Zombie.Reanimate(random.randint(player.ballx-600,player.ballx-450), False,i) # and instead of adding new data to lists, it just changes the data of the one that died so 
                else:                   # all the loops sync correctly causing no errors with the bullet fly functionality
                    Zombie.Reanimate(random.randint(player.ballx+450,player.ballx+600), False,i) 
            if score > 15:
                if LeftorRightZ[random.randint(0,1)]:
                    Zombie.Reanimate(random.randint(player.ballx-500,player.ballx-450), LeftorRightZ[random.randint(0,1)],i) 
                else:
                    Zombie.Reanimate(random.randint(player.ballx+400,player.ballx+450), LeftorRightZ[random.randint(0,1)],i) 
            Zombie.Health[i] = 5 # Health controls if this zombie is in the Game Still
########################################################## Axe and BulletFly
        if inventory == 2: # Axe holding
            P.AxeH(P.ballx+10, P.bally)
            if not(Zombie.Hunter[i]):
                if P.Stamina > 0: 
                    if AxeAttack and areaZ <= 60:
                        P.Stamina -= 1
                        pygame.mixer.Sound.play(BlockTearDown)
                        if Zombie.Health[i] >= 0:
                            Zombie.Health[i] = Zombie.Health[i] - 2.5 # Damage
                            for x in range(0,50): 
                                gameDisplay.blit(bg1, (bgX1, 0)) 
                                gameDisplay.blit(bg, (bgX, 0))
                                gameDisplay.blit(bg2, (bgX2, 0))
                                P.AxeW(P.ballx, P.bally)
                                #P.redrawPlayer(P.ballx, P.bally)
                                if Zombie.cright[i]:
                                    if Zombie.Health[i] >= 0:
                                        gameDisplay.blit(Zombie.DamageR, (Zombie.crawlx[i],Zombie.crawly))
                                else:
                                    if Zombie.Health[i] >= 0:
                                        gameDisplay.blit(Zombie.DamageL, (Zombie.crawlx[i],Zombie.crawly))
                                pygame.display.update()
                        AxeAttack = False
        
            

        if bulletfly: # BulletFly
            
            if not(P.direction): 
                bullet_changex = -5 # bullet direction with player direction
            if P.direction:
                bullet_changex = 5
            bulletx += bullet_changex
            if not(P.direction):
                things(bulletx, P.bally+35, 5, red) # bullet spawn
                
            else:
                things(bulletx+45, P.bally+35, 5, red)
                
                
            if Zombie.Health[i] >= 0: # zombie alive
                if(areaBullet <= 45): # if hit zombie
                    if not(Zombie.Hunter[i]):
                        if Zombie.cright[i]:
                            gameDisplay.blit(Zombie.DamageR, (Zombie.crawlx[i],Zombie.crawly))
                        else:
                            gameDisplay.blit(Zombie.DamageL, (Zombie.crawlx[i],Zombie.crawly))
                        bulletx = P.ballx+10 # reset bullet positions
                        Zombie.Health[i] = Zombie.Health[i] - 2.5 # Damage
                    else:
                        bulletx = P.ballx+10 # reset bullet positions
                        Zombie.Health[i] = Zombie.Health[i] - 5 # Damage
                    bullet_changex = 0
                    bulletfly = False
                if(bulletx <= 10): # Bullet Boundaries 
                    bulletx = P.ballx+10 # reset bullet positions
                    bullet_changex = 0
                    bulletfly = False
                if(bulletx >= 750):
                    bulletx = P.ballx+10 # reset bullet positions
                    bullet_changex = 0
                    bulletfly = False
            else:
                if(bulletx <= 10): # Bullet Boundaries 
                    bulletx = P.ballx+10 # reset bullet positions
                    bullet_changex = 0
                    bulletfly = False
                if(bulletx >= 750):
                    bulletx = P.ballx+10 # reset bullet positions
                    bullet_changex = 0 
                    bulletfly = False
###########################################################################        
    
    if inventory == 2: # Axe holding
        if not(AxeAttack):
            P.AxeH(P.ballx+10, P.bally)
        if AxeAttack and areaDrink <= 100:
            for x in range(0,100):
                gameDisplay.blit(bg1, (bgX1, 0)) 
                gameDisplay.blit(bg, (bgX, 0))
                gameDisplay.blit(bg2, (bgX2, 0))
                P.AxeW(P.ballx, P.bally)
                P.redrawPlayer(P.ballx, P.bally)
                for i in range(BLOCKS.Blocks):   
                    gameDisplay.blit(BLOCKS.Block, (BLOCKS.Blockx[i], BLOCKS.Blocky[i])) 
                pygame.display.update()
            P.Stamina += 7
            LeftorRightZ = [True, False]
            if LeftorRightZ[random.randint(0,1)]: #SPAWN
                Drinkx = P.ballx-1000
            else:
                Drinkx = P.ballx+1000
            AxeAttack = False
        if AxeAttack and areaTree <= 100:
            for x in range(0,100):
                gameDisplay.blit(bg1, (bgX1, 0)) 
                gameDisplay.blit(bg, (bgX, 0))
                gameDisplay.blit(bg2, (bgX2, 0))
                P.AxeW(P.ballx, P.bally)
                P.redrawPlayer(P.ballx, P.bally)
                for i in range(BLOCKS.Blocks):   
                    gameDisplay.blit(BLOCKS.Block, (BLOCKS.Blockx[i], BLOCKS.Blocky[i])) 
                pygame.display.update()
            if TreeS == 0:
                P.Wood += .8 # get block from hitting tree
            else:
                P.Wood += .5
            LeftorRightZ = [True, False]
            if LeftorRightZ[random.randint(0,1)]: #SPAWN
                Treex = P.ballx-1000 # Spawn new Tree
            else:
                Treex = P.ballx+1000 # Spawn new Tree
            TreeS = random.randint(0,2)
            AxeAttack = False
        

    if inventory == 0: # Block Holding
        P.HoldB()
        
    bgX1 += bgX1_change
    bgX += bgX_change
    bgX2 += bgX2_change


    if bgX1 < -2560: # making them all reset at the same third image to the left's minimum x
        bgX1 = bg.get_width()
    if bgX < -2560: 
        bgX = bg.get_width() 
    if bgX2 < -2560: 
        bgX2 = bg.get_width()

    if bgX1 > 2560: # making them all reset at the same third image to the right's max x
        bgX1 = bg.get_width() * -1
    if bgX > 2560: 
        bgX = bg.get_width()  * -1
    if bgX2 > 2560: 
        bgX2 = bg.get_width() * -1

    P.redrawPlayer(P.ballx, P.bally) # player

    for i in range(BLOCKS.Blocks):    # Display WORKS
        gameDisplay.blit(BLOCKS.Block, (BLOCKS.Blockx[i], BLOCKS.Blocky[i]))
        if BLOCKS.Health[i] == 0:
            BLOCKS.Blockx[i] = 0
            BLOCKS.Blocky[i] = 5000 # erase
            

    Tree.TreeSpawn(Treex,TreeS) # Trees
    Energy.DrinkSpawn(Drinkx)
            
    pygame.display.update()
    clock.tick(65)

pygame.quit()
quit()


