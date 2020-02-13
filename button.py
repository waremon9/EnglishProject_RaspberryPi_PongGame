import pygame

class Button(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, screen, color, Yposition, SIZEX):
        super().__init__()

        pygame.draw.line(screen, color, [SIZEX/2-102, Yposition-40], [SIZEX/2+102, Yposition-40], 5)
        pygame.draw.line(screen, color, [SIZEX/2+100, Yposition-40], [SIZEX/2+100, Yposition+40], 5)
        pygame.draw.line(screen, color, [SIZEX/2+102, Yposition+40], [SIZEX/2-102, Yposition+40], 5)
        pygame.draw.line(screen, color, [SIZEX/2-100, Yposition+40], [SIZEX/2-100, Yposition-40], 5)
