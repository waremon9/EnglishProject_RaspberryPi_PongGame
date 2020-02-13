# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
from bonus import Bonus
from button import Button
import time
from random import randint
#comment for PC use
import ft5406

#comment for PC use
ts = ft5406.Touchscreen()

#pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

#pop = pygame.mixer.Sound('POP.wav')
#pygame.mixer.music.load('Musique.wav')
#pygame.mixer.music.play(-1)
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LAVENDER = (230,230,250)
CYAN = (0,173,238)
LIGHT_RED = (255,60,60)
LIGHT_BLUE=(60,60,255)
LIGHT_LIGHT_BLUE = (100,100,255)
LIGHT_GREEN = (60,255,60)

#List that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Open a new window
SIZEX = 780
SIZEY = 460
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Pong")
 
paddleA = Paddle(WHITE, 10, 99, SIZEY+10)
paddleA.rect.x = 30
paddleA.rect.y = (SIZEY+10)/2-50
 
paddleB = Paddle(WHITE, 10, 99, SIZEY+10)
paddleB.rect.x = SIZEX-20
paddleB.rect.y = (SIZEY+10)/2-50
 
ball = Ball(WHITE,9,9)
ball.rect.x = (SIZEX+10)/2-5
ball.rect.y = (SIZEY+10)/2-5

bonusA = Bonus(RED, SIZEX+10, SIZEY+10, all_sprites_list)
bonusB = Bonus(GREEN, SIZEX+10, SIZEY+10, all_sprites_list)
bonusC = Bonus(BLUE, SIZEX+10, SIZEY+10, all_sprites_list)
 
# Add the paddles and the ball to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

#keep the ball velocity for unpause
ballxpause = 0
ballypause = 0

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def onButtonPress(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] and mouse[0] > x and y + h > mouse[1] and mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                pygame.mouse.set_visible(False)
                return 1
            elif action == "quit":
                return 0
            elif action == "setting":
                pygame.mouse.set_visible(True)
                return 2
            elif action == "menu":
                pygame.mouse.set_visible(True)
                return 3
            elif action == "continue":
                pygame.mouse.set_visible(False)
                return 4
            elif action == "new":
                pygame.mouse.set_visible(False)
                return 5
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont(None, 48)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

#define the function who draw menu
def menuPrincipal():
    screen.fill(BLACK)
    #text
    font = pygame.font.Font(None, 74)
    text = font.render('PONG', 1, WHITE)
    screen.blit(text, (int(SIZEX/2)-75,40))
    #buttons
    Button(screen, WHITE, 170, SIZEX)
    Button(screen, WHITE, 290, SIZEX)
    Button(screen, WHITE, 410, SIZEX)
    #real button
    quit1 = onButtonPress("Quit", SIZEX/2-97, 373, 195, 75, RED, LIGHT_RED, "quit")
    play = onButtonPress("PLAY!", SIZEX/2-97, 133, 195, 75, GREEN, LIGHT_GREEN, "play")
    pygame.display.flip()
    if quit1 != None:
        return quit1
    if play != None:
        return play
    if setting != None:
        return setting

def menuPause():
    screen.fill(BLACK)
    #text
    font = pygame.font.Font(None, 74)
    text = font.render('Game paused', 1, WHITE)
    screen.blit(text, (int(SIZEX/2)-170,40))
    #buttons
    Button(screen, WHITE, 170, SIZEX)
    Button(screen, WHITE, 290, SIZEX)
    #real button
    menu = onButtonPress("Menu", SIZEX/2-97, 133, 195, 75, RED, LIGHT_RED, "menu")
    cont = onButtonPress("Continue", SIZEX/2-97, 253, 195, 75, GREEN, LIGHT_GREEN, "continue")
    pygame.display.flip()
    if menu != None:
        return menu
    if cont != None:
        return cont

def menuVictory():
    screen.fill(BLACK)
    #text
    x='P1'
    font = pygame.font.Font(None, 100)
    text = font.render(x+' WIN !!!', 1, WHITE)
    screen.blit(text, (int(SIZEX/2)-150,70))
    #buttons
    Button(screen, WHITE, 250, SIZEX)
    Button(screen, WHITE, 400, SIZEX)
    #real button
    menu = onButtonPress("Menu", SIZEX/2-97, 363, 195, 75, RED, LIGHT_RED, "menu")
    new = onButtonPress("New Game", SIZEX/2-97, 213, 195, 75, GREEN, LIGHT_GREEN, "new")
    pygame.display.flip()
    if menu != None:
        return menu
    if new != None:
        return new

def resetGame():
    global scoreA, scoreB, ball
    ball.velocity[0] = 4
    ball.rect.x = (SIZEX+10)/2-5
    ball.rect.y = (SIZEY+10)/2-5
    #Initialise player scores
    scoreA = 0
    scoreB = 0
    paddleA.rect.y = (SIZEY+10)/2-50
    paddleB.rect.y = (SIZEY+10)/2-50

def stopGame():
    global ball, ballypause,ballxpause
    if(ball.velocity[0]!=0):
        ballxpause = ball.velocity[0]
        ballypause = ball.velocity[1]
    ball.velocity[0] = 0
    ball.velocity[1] = 0

def unpauseGame():
    global ball, ballypause,ballxpause
    ball.velocity[0] = ballxpause
    ball.velocity[1] = ballypause

 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

#Initialise player scores
scoreA = 0
scoreB = 0

#other variable
speedPaddleA = 8
speedPaddleB = 8
cooldownPA = -1
cooldownPB = -1

Play = False
Menu = True
Pause = False
Victory = False
Setting = False

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
 
    #Moving the paddles when the users touch the screen
    sumYP1 = 0
    nbYP1 = 0
    sumYP2 = 0
    nbYP2 = 0
    
#comment for PC use from here:
    #get the touch
    for touch in ts.poll():
        
        #Only the valid one (actually touching)
        if(touch.valid):
            #check the pause
            if((SIZEX/2-50)<touch.x<(SIZEX/2-30)  and 25<touch.y<52):
                Pause = True
                Play = False
                pygame.mouse.set_visible(True)
                
            if touch.x < SIZEX/2:
                sumYP1 += touch.y
                if touch.slot>0:
                    sumYP1 += touch.y
                nbYP1 += 1
            else :
                sumYP2 += touch.y
                if touch.slot>0:
                    sumYP2 += touch.y
                nbYP2 += 1
               
        if nbYP1 == 0 :
            nbYP1 = 1
        if nbYP2 == 0 :
            nbYP2 = 1
            
        finalYP1 = int(sumYP1/nbYP1)
        finalYP2 = int(sumYP2/nbYP2)
    
        if finalYP1<=paddleA.padY()+50 and sumYP1!=0:
            paddleA.moveUp(speedPaddleA)
        elif finalYP1>=paddleA.padY()+50 and sumYP1!=0:
            paddleA.moveDown(speedPaddleA)

        if finalYP2<=paddleB.padY()+50 and sumYP2!=0:
            paddleB.moveUp(speedPaddleB)
        elif finalYP2>=paddleB.padY()+50 and sumYP2!=0:
            paddleB.moveDown(speedPaddleB)
#to here

#uncomment for PC use from here:
##    keys = pygame.key.get_pressed()
##    if keys[pygame.K_w]:
##        paddleA.moveUp(speedPaddleA)
##    if keys[pygame.K_s]:
##        paddleA.moveDown(speedPaddleA)
##    if keys[pygame.K_UP]:
##        paddleB.moveUp(speedPaddleB)
##    if keys[pygame.K_DOWN]:
##        paddleB.moveDown(speedPaddleB)
#to here


    # --- Game logic should go here
    all_sprites_list.update()
 
    #Check if the ball is bouncing against any of the 4 walls:
    #check the sides
    if ball.rect.x>=SIZEX+5 or ball.rect.x<=5:
        if ball.rect.x>=SIZEX-5:
            scoreA+=1
            ball.velocity[0] = -4
        if ball.rect.x<=5:
            scoreB+=1
            ball.velocity[0] = 4
        time.sleep(1)
        ball.rect.x = 400
        ball.rect.y = 240
        ball.velocity[1] = 0
        paddleA.reset(all_sprites_list)
        paddleB.reset(all_sprites_list)
        speedPaddleA = 8
        speedPaddleB = 8
        cooldownPA = -1
        cooldownPB = -1

    #check up and down
    if ball.rect.y>SIZEY+5 and ball.velocity[1]>0:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<10 and ball.velocity[1]<0:
        ball.rect.y=10
        ball.velocity[1] = -ball.velocity[1] 

    #Detect collisions between the ball and the paddles and check malus/bonus cooldown
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        #pygame.mixer.Sound.play(pop)
        if(cooldownPA>0):
            cooldownPA-=1
        elif(cooldownPA==0):
            cooldownPA=-1
            paddleA.reset(all_sprites_list)
        if(cooldownPB>0):
            cooldownPB-=1
        elif(cooldownPB==0):
            cooldownPB=-1
            paddleB.reset(all_sprites_list)
        if (ball.velocity[0] > 0):
            ball.bounce(paddleB)	
        else:
            ball.bounce(paddleA)

    #Detect collisions between the ball and the bonusA (RED)
    if pygame.sprite.collide_mask(ball, bonusA):
        bonusA.move(SIZEX, SIZEY)
        if (ball.velocity[0] > 0):
            paddleB.changeSize(all_sprites_list, -18)
            cooldownPB = 6
        else:
            paddleA.changeSize(all_sprites_list, -18)
            cooldownPA = 6

    #Detect collisions between the ball and the bonusB (GREEN)
    if pygame.sprite.collide_mask(ball, bonusB):
        bonusB.move(SIZEX, SIZEY)
        if (ball.velocity[0] > 0):
            paddleA.changeSize(all_sprites_list, 18)
            cooldownPB = 8
        else:
            paddleB.changeSize(all_sprites_list, 18)
            cooldownPA = 8

    #Detect collisions between the ball and the bonusC (BLUE)
    if pygame.sprite.collide_mask(ball, bonusC):
        bonusC.move(SIZEX, SIZEY)
        if (ball.velocity[0] > 0):
            if(speedPaddleB<0):
                speedPaddleB = 2
                paddleB.image.fill(WHITE)
            else:
                speedPaddleB = -2
                paddleB.image.fill(CYAN)
        else:
            if(speedPaddleA<0):
                speedPaddleA = 2
                paddleA.image.fill(WHITE)
            else:
                speedPaddleA = -2
                paddleA.image.fill(CYAN)
      
    # --- Drawing code should go here
    if Play == True:
        # First, clear the screen to black. 
        screen.fill(BLACK)
        #Draw the net
        pygame.draw.line(screen, WHITE, [(SIZEX+10)/2-1, 30], [(SIZEX+10)/2-1, SIZEY-10], 5)
        
        #Draw the arena
        pygame.draw.line(screen, LAVENDER, [0, 5], [SIZEX+20, 5], 10)
        pygame.draw.line(screen, LAVENDER, [SIZEX+15, 5], [SIZEX+15, SIZEY+15], 10)
        pygame.draw.line(screen, LAVENDER, [SIZEX+20, SIZEY+15], [0, SIZEY+15], 10)
        pygame.draw.line(screen, LAVENDER, [4, SIZEY+15], [4, 5], 10)
        
        #draw pause Button
        pygame.draw.line(screen, WHITE, [SIZEX/2-50, 25], [SIZEX/2-50, 52], 8)
        pygame.draw.line(screen, WHITE, [SIZEX/2-30, 25], [SIZEX/2-30, 52], 8)
               
        #Draw all the sprites
        all_sprites_list.draw(screen) 

        #Display scores:
        font = pygame.font.Font(None, 74)
        text = font.render(str(scoreA), 1, WHITE)
        screen.blit(text, (int(SIZEX/3)-10,10))
        text = font.render(str(scoreB), 1, WHITE)
        screen.blit(text, (int(2*SIZEX/3)-10,10))
        pygame.display.flip()
        if scoreA >= 11 or scoreB >= 11:
            pygame.mouse.set_visible(True)
            Play = False
            Victory = True
 
    # game or menu
    if Play == False:
        stopGame()
        if Menu == True:
            chose = menuPrincipal()
            if chose == 0:
                carryOn = False
            elif chose == 1:
                resetGame()
                time.sleep(0.5)
                Play = True
                Menu = False
            elif chose == 2:
                Menu = False
                Setting = True
        
        elif Pause == True:
            chose = menuPause()
            if chose == 3:
                time.sleep(0.5)
                Pause = False
                Menu = True
            elif chose == 4:
                unpauseGame()
                Play = True
                Pause = False
                
            elif Setting == True:
                setting()
            

        elif Victory == True:
            chose = menuVictory()
            if chose == 3:
                time.sleep(0.5)
                Victory = False
                Menu = True
            elif chose == 5:
                resetGame()
                Play = True
                Victory = False
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#stop the game engine when main program exited
pygame.quit()

