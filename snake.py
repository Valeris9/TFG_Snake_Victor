import pygame

class Snake:

    #This is the constructor of the class.
    def __init__(self):
        self.size = 20
        self.x, self.y = 0, 0
        self.speed = 20
        self.direction = "RIGHT"
        self.body = [(self.x, self.y)]

    #This method is used to draw the snake on the screen.
    def handle_keys(self, keys):
        if keys[pygame.K_UP] and self.direction != "DOWN":
            self.direction = "UP"
        elif keys[pygame.K_DOWN] and self.direction != "UP":
            self.direction = "DOWN"
        elif keys[pygame.K_LEFT] and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif keys[pygame.K_RIGHT] and self.direction != "LETF":
            self.direction = "RIGHT"

    #This method is used to move the snake.
    def move(self):
        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed
        self.body.append((self.x, self.y))
        self.body = self.body[-1:]

    #This method is used to draw the snake on the screen.
    def draw(self, win):
        for segment in self.body:
            pygame.draw.rect(win,(0,255,0),(segment[0], segment[1], self.size, self.size))

    #This method is used to check if the snake has collided with the food.
    def check_collision(self, food):
        if self.x == food.x and self.y == food.y:
            return True
        else:
            return False