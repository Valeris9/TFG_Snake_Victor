from enum import Enum
import pygame

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

    #This is the constructor of the class.
    def __init__(self, block_size, boundary):
        self.block_size = block_size
        self.boundary = boundary
        self.respawn()

    def respawn(self):
        self.length = 2
        self.direction = Direction.RIGHT
        self.body = [(20, 20), (20, 40), (20, 60)]

    def update_score(self):
        self.score += 1

    #This method is used to draw the snake on the screen.
    def steer(self, direction):
        if self.direction == Direction.DOWN and direction != Direction.UP:
            self.direction = direction
        elif self.direction == Direction.UP and direction != Direction.DOWN:
            self.direction = direction
        elif self.direction == Direction.LEFT and direction != Direction.RIGHT:
            self.direction = direction
        elif self.direction == Direction.RIGHT and direction != Direction.LEFT:
            self.direction = direction

    #This method is used to move the snake.
    def move(self):
        global next_head
        curr_head = self.body[-1]
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

    #This method is used to draw the snake on the screen.
    def draw(self, game, win):
        for segment in self.body:
            pygame.draw.rect(win,self.color,(segment[0], segment[1], self.block_size, self.block_size))

    #This method is used to check if the snake has collided with the food.
    def check_collision_food(self, food):
        head = self.body[-1]
        #print(f"Checking collision: Head at {head}, Food at ({food.x}, {food.y})")
        if head[0] == food.x and head[1] == food.y:
            self.eat()
            food.respawn()
            print("Food eaten")
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


