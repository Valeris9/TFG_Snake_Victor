import pygame
from food import Food
from game import *

class MainHuman:
    def __init__(self):
        pygame.init()

        self.boundary = (800, 600)
        self.win = pygame.display.set_mode(self.boundary)
        pygame.display.set_caption("Snake Game")

        self.block_size = 20
        self.snake = Snake(self.block_size, self.boundary)
        self.food = Food(self.block_size, self.boundary)
        self.font = pygame.font.SysFont('Times New Roman', 60, True)
        self.font_small = pygame.font.SysFont('Times New Roman', 20, True)

    def run_game(self):
        run = True
        while run:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.snake.steer(Direction.LEFT)
            elif keys[pygame.K_RIGHT]:
                self.snake.steer(Direction.RIGHT)
            elif keys[pygame.K_UP]:
                self.snake.steer(Direction.UP)
            elif keys[pygame.K_DOWN]:
                self.snake.steer(Direction.DOWN)

            self.snake.move()
            self.snake.check_collision_food(self.food)

            if self.snake.check_collision_boundary() or self.snake.check_collision_tail():
                text = self.font.render('Game Over', True, (255, 255, 255))
                text_rect = text.get_rect(center=(self.boundary[0] / 2, self.boundary[1] / 2))
                self.win.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(2000)
                self.snake.respawn()
                self.food.respawn()

            self.win.fill((0, 0, 0))
            self.snake.draw(pygame, self.win)
            self.food.draw(pygame, self.win)

            score_text = self.font_small.render(f'Score: {self.snake.score}', True, (255, 255, 255))
            self.win.blit(score_text, (10, 10))
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = MainHuman()
    game.run_game()

