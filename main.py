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
font = pygame.font.SysFont('Times New Roman', 60, True)
font_small = pygame.font.SysFont('Times New Roman', 20, True)

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

    if snake.check_collision_boundary() == True or snake.check_collision_tail() == True:
        text = font.render('Game Over', True, (255, 255, 255))
        text_rect = text.get_rect(center=(boundary[0] / 2, boundary[1] / 2))
        win.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        snake.respawn()
        food.respawn()

    win.fill((0, 0, 0))
    snake.draw(pygame, win)
    food.draw(pygame, win)

    score_text = font_small.render(f'Score: {snake.score}', True, (255, 255, 255))
    win.blit(score_text, (10, 10))
    pygame.display.flip()

pygame.quit()
