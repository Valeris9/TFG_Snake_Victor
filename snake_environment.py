import numpy as np
import torch

from food import Food
from game import Snake


class SnakeEnvironment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = Snake(block_size=20, boundary=(width, height))
        self.food = Food(size=20, boundary=(width, height))
        self.game_over = False

    def reset(self):
        self.snake.respawn()
        self.food.respawn()
        self.game_over = False
        return self.get_state()

    def get_state(self):
        state = np.zeros((self.width // 20, self.height // 20), dtype=np.int8)
        for segment in self.snake.body:
            state[segment[0] // 20, segment[1] // 20] = 1
        state[self.food.x // 20, self.food.y // 20] = 2
        return torch.tensor(state.flatten(), dtype=torch.float)

    def step(self, action):
        if action == 0:
            self.snake.steer(self.snake.direction.UP)
        elif action == 1:
            self.snake.steer(self.snake.direction.DOWN)
        elif action == 2:
            self.snake.steer(self.snake.direction.LEFT)
        elif action == 3:
            self.snake.steer(self.snake.direction.RIGHT)

        self.snake.move()
        self.snake.check_collision_food(self.food)

        if self.snake.check_collision_boundary() or self.snake.check_collision_tail():
            self.game_over = True
            reward = -1
        elif len(self.snake.body) == self.width * self.height:
            self.game_over = True
            reward = 1
        else:
            reward = 0

        return self.get_state(), reward, self.game_over

    def play_step(self, action):
        state, reward, game_over = self.step(action)
        return state, reward, game_over