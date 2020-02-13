import pygame
BLACK = (0,0,0)
 
class Ball(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.velocity = [4,0]
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
    
    #update the position of the ball
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    #every time the ball hit a paddle, it bounce and accelerate (capped at 15)
    def bounce(self, paddle):
        if(self.velocity[0]>-15 and self.velocity[0]<15):
            if(self.velocity[0]>0):
                self.velocity[0] = -self.velocity[0]-1
            else:
                self.velocity[0] = -self.velocity[0]+1
        else:
            self.velocity[0] = -self.velocity[0]
        #the ball direction depend of where it hit the paddle.
        partSize = paddle.size/9
        ballY = self.rect.y+5
        paddleY = paddle.rect.y
        hit = ballY - paddleY
        partHit = hit/partSize
        self.velocity[1] = (partHit-4)*2
        
