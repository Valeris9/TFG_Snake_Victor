import pygame
import random

class Food:
    def __init__(self):
        self.size = 20
        self.x = random.randrange(0, 800, self.size)
        self.y = random.randrange(0, 600, self.size)
        self.color = (255, 0, 0)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))