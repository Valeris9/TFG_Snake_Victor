from enum import Enum
import pygame
import numpy as np

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Snake:
    length = None
    direction = None
    body = None
    block_size = None
    color = (0, 255, 0)
    boundary = None
    score = 0
    start_time = None

    def __init__(self, block_size, boundary):
        self.block_size = block_size
        self.boundary = boundary
        self.respawn()

    def respawn(self):
        self.length = 4
        self.direction = Direction.RIGHT
        self.body = [(20, 20), (40, 20), (60, 20), (80, 20)]
        self.score = 0

    def update_score(self):
        self.score += 1

    def steer(self, action):
        if isinstance(action, list):  # Verifica si la acción viene de la IA
            if np.array_equal(action, [1, 0, 0, 0]) and self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
            elif np.array_equal(action, [0, 1, 0, 0]) and self.direction != Direction.UP:
                self.direction = Direction.DOWN
            elif np.array_equal(action, [0, 0, 1, 0]) and self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
            elif np.array_equal(action, [0, 0, 0, 1]) and self.direction != Direction.DOWN:
                self.direction = Direction.UP
        else:  # Acción de control humano
            if action == Direction.RIGHT and self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
            elif action == Direction.DOWN and self.direction != Direction.UP:
                self.direction = Direction.DOWN
            elif action == Direction.LEFT and self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
            elif action == Direction.UP and self.direction != Direction.DOWN:
                self.direction = Direction.UP

    def move(self):
        curr_head = self.body[-1]
        next_head = curr_head  # Inicialización de next_head para evitar errores

        if self.direction == Direction.DOWN:
            next_head = (curr_head[0], curr_head[1] + self.block_size)
        elif self.direction == Direction.UP:
            next_head = (curr_head[0], curr_head[1] - self.block_size)
        elif self.direction == Direction.RIGHT:
            next_head = (curr_head[0] + self.block_size, curr_head[1])
        elif self.direction == Direction.LEFT:
            next_head = (curr_head[0] - self.block_size, curr_head[1])

        self.body.append(next_head)
        if len(self.body) > self.length:
            self.body.pop(0)

    def draw(self, game, win):
        for segment in self.body:
            pygame.draw.rect(win, self.color, (segment[0], segment[1], self.block_size, self.block_size))

    def check_collision_food(self, food):
        head = self.body[-1]
        if head[0] == food.x and head[1] == food.y:
            self.eat()
            return True
        return False

    def eat(self):
        self.length += 1
        self.update_score()


    def check_collision_tail(self):
        head = self.body[-1]
        return any(head == segment for segment in self.body[:-1])

    def check_collision_boundary(self):
        head = self.body[-1]
        if head[0] >= self.boundary[0] or head[0] < 0 or head[1] >= self.boundary[1] or head[1] < 0:
            return True
        return False
