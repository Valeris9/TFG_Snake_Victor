import pygame
import random

class Food:
    size = None
    color = (255, 0, 0)
    x = 0
    y = 0
    boundary = None
    def __init__(self, size, boundary):
        self.size = size
        self.boundary = boundary

    def draw(self, game, win):
        game.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def respawn(self):
        block_x = (self.boundary[0])/self.size
        block_y = (self.boundary[1])/self.size

        self.x = random.randint(0, block_x-1)*self.size
        self.y = random.randint(0, block_y-1)*self.size

