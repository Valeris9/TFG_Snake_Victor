import pygame

from food import Food
from snake import Snake

pygame.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

snake = Snake()
food = Food()

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    snake.handle_keys(keys)

    snake.move()
    snake.check_collision(food)

    win.fill((0, 0, 0))
    snake.draw(win)
    food.draw(win)

    pygame.display.update()
    clock.tick(10)

pygame.quit()