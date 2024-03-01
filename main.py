import pygame

from food import Food
from game import *


pygame.init()

boundary = (800, 600)
win = pygame.display.set_mode(boundary)
pygame.display.set_caption("Snake Game")

block_size = 20
snake = Snake(block_size, boundary)
food = Food(block_size, boundary)

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake.steer(Direction.LEFT)
    elif keys[pygame.K_RIGHT]:
        snake.steer(Direction.RIGHT)
    elif keys[pygame.K_UP]:
        snake.steer(Direction.UP)
    elif keys[pygame.K_DOWN]:
        snake.steer(Direction.DOWN)

    snake.move()
    snake.check_collision_food(food)

    win.fill((0, 0, 0))
    snake.draw(pygame, win)
    food.draw(pygame, win)
    pygame.display.flip()


pygame.quit()