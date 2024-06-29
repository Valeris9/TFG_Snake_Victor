import pygame
from snake import Snake, Direction
from food import Food

# Ajusta los valores de la ventana del juego
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BLOCK_SIZE = 20


def game_loop():
    pygame.init()
    display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake(BLOCK_SIZE, (WINDOW_WIDTH, WINDOW_HEIGHT))
    food = Food(BLOCK_SIZE, (WINDOW_WIDTH, WINDOW_HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.steer(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.steer(Direction.RIGHT)
                elif event.key == pygame.K_UP:
                    snake.steer(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    snake.steer(Direction.DOWN)

        snake.move()

        if snake.check_collision_food(food):
            print("Food eaten")
            food.respawn()

        if snake.check_collision_tail() or snake.check_collision_boundary():
            running = False

        display.fill((0, 0, 0))
        snake.draw(display, display)
        food.draw(pygame, display)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
