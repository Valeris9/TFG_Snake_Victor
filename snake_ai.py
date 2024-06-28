import pygame
import random
from enum import Enum
from collections import namedtuple
from snake import Snake
from food import Food

Point = namedtuple('Point', 'x, y')


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.snake = Snake(block_size=20, boundary=(self.w, self.h))
        self.food = Food(size=20, boundary=(self.w, self.h))
        self.frame_iteration = 0

    def reset(self):
        self.snake.respawn()
        self.food.respawn()
        self.frame_iteration = 0
        self.snake.score = 0

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.snake.steer(action)
        self.snake.move()
        #print(f"Snake moved to: {self.snake.body[-1]}")

        reward = 0
        game_over = False

        if self.snake.check_collision_boundary() or self.snake.check_collision_tail() or self.frame_iteration > 100 * len(
                self.snake.body):
            game_over = True
            reward = -10
            return reward, game_over, self.snake.score

        if self.snake.check_collision_food(self.food):
            reward = 10
            self.food.respawn()

        self._update_ui()
        self.clock.tick(40)  # Controlar la velocidad del juego
        return reward, game_over, self.snake.score

    def _update_ui(self):
        self.display.fill((0, 0, 0))
        for pt in self.snake.body:
            pygame.draw.rect(self.display, self.snake.color,
                             pygame.Rect(pt[0], pt[1], self.snake.block_size, self.snake.block_size))
        self.food.draw(pygame, self.display)
        pygame.display.flip()

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.snake.body[-1]
        if pt[0] >= self.w or pt[0] < 0 or pt[1] >= self.h or pt[1] < 0:
            return True
        if pt in self.snake.body[:-1]:
            return True
        return False
