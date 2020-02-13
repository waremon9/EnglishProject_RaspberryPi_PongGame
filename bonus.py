import pygame
from random import randint
BLACK = (0,0,0)

class Bonus(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, SIZEX, SIZEY, liste):
        super().__init__()
        
        # Pass in the color of the car, and its x and y position.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([15, 15])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, 17, 17])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

        liste.add(self)
        
        self.move(SIZEX, SIZEY)

    #randomly move the bonus
    def move(self, SIZEX, SIZEY):
        x=randint(200, SIZEX-215)
        y=randint(40,SIZEY-55)
        self.rect.x=x
        self.rect.y=y
