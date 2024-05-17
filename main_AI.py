import os

import pygame
from food import Food
from snake import Snake, Direction
from agent import Agent

class MainRL:
    def __init__(self):
        pygame.init()
        self.boundary = (800, 600)
        self.win = pygame.display.set_mode(self.boundary)
        pygame.display.set_caption("Snake Game with RL")

        self.block_size = 20
        self.snake = Snake(self.block_size, self.boundary)
        self.food = Food(self.block_size, self.boundary)
        self.agent = Agent(11, 4)

        model_path = "snake_model.pth"
        if os.path.exists(model_path):
            self.agent.load_model(model_path)
            print("Model loaded from snake_model.pth")

        with open("rewards.txt", "w") as f:
            f.write("")

    def get_state(self):
        head_x, head_y = self.snake.body[-1]
        food_x, food_y = self.food.x, self.food.y

        # Distancia a la comida
        distance_to_food_x = (food_x - head_x) / self.block_size
        distance_to_food_y = (food_y - head_y) / self.block_size

        danger_straight = self.is_danger_straight()
        danger_left = self.is_danger_left()
        danger_right = self.is_danger_right()

        state = [
            distance_to_food_x,  # Distancia a la comida en el eje X
            distance_to_food_y,  # Distancia a la comida en el eje Y
            danger_straight,  # Peligro al frente
            danger_left,  # Peligro a la izquierda
            danger_right,  # Peligro a la derecha
            self.snake.direction == Direction.RIGHT,
            self.snake.direction == Direction.LEFT,
            self.snake.direction == Direction.DOWN,
            self.snake.direction == Direction.UP
        ]

        return state

    def reset(self):
        self.snake = Snake(self.block_size, self.boundary)
        self.food = Food(self.block_size, self.boundary)
        return self.get_state()

    def step(self, action):
        self.snake.steer(Direction(action + 1))
        self.snake.move()

        # Check collision with food
        if self.snake.check_collision_food(self.food):
            reward = 1
        else:
            reward = 0

        done = self.snake.check_collision_boundary() or self.snake.check_collision_tail()
        if done:
            reward = -1
            self.snake.respawn()
            self.food.respawn()

        next_state = self.get_state()
       #print(f"Action: {action}, Reward: {reward}, Done: {done}")
        return next_state, reward, done, None

    def is_danger_straight(self):
        head = self.snake.body[-1]
        next_pos = self.get_next_position(head, self.snake.direction)
        return self.is_collision(next_pos)

    def is_danger_left(self):
        head = self.snake.body[-1]
        next_direction = self.turn_left(self.snake.direction)
        next_pos = self.get_next_position(head, next_direction)
        return self.is_collision(next_pos)

    def is_danger_right(self):
        head = self.snake.body[-1]
        next_direction = self.turn_right(self.snake.direction)
        next_pos = self.get_next_position(head, next_direction)
        return self.is_collision(next_pos)

    def get_next_position(self, position, direction):
        x, y = position
        if direction == Direction.UP:
            y -= self.block_size
        elif direction == Direction.DOWN:
            y += self.block_size
        elif direction == Direction.LEFT:
            x -= self.block_size
        elif direction == Direction.RIGHT:
            x += self.block_size
        return (x, y)

    def is_collision(self, position):
        x, y = position
        if x < 0 or x >= self.boundary[0] or y < 0 or y >= self.boundary[1]:
            return True
        if position in self.snake.body:
            return True
        return False

    def turn_left(self, direction):
        turn_left_map = {
            Direction.UP: Direction.LEFT,
            Direction.DOWN: Direction.RIGHT,
            Direction.LEFT: Direction.DOWN,
            Direction.RIGHT: Direction.UP
        }
        return turn_left_map[direction]

    def turn_right(self, direction):
        turn_right_map = {
            Direction.UP: Direction.RIGHT,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
            Direction.RIGHT: Direction.DOWN
        }
        return turn_right_map[direction]

    def train_agent(self, episodes=500):
        total_rewards = []
        for e in range(episodes):
            state = self.reset()
            total_reward = 0
            self.win.fill((0, 0, 0))  # Limpia la pantalla

            while True:
                action = self.agent.act(state)
                next_state, reward, done, _ = self.step(action)
                self.agent.remember(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward

                # Actualizaciones de la pantalla
                self.win.fill((0, 0, 0))
                self.snake.draw(pygame, self.win)
                self.food.draw(pygame, self.win)
                pygame.display.flip()
                pygame.time.delay(50)

                if done:
                    break

            total_rewards.append(total_reward)
            print(f"Episodio: {e + 1}/{episodes}, Recompensa: {total_reward}, Exploración: {self.agent.epsilon:.2f}")
            self.agent.replay(64)

            with open("rewards.txt", "a") as f:
                f.write(f"{total_reward}\n")

            if e % 10 == 0:
                self.agent.save_model("snake_model.pth")
                print(f"Model saved to snake_model.pth at episode {e}")
        self.agent.save_model("snake_model.pth")

    def run_game(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            state = self.get_state()
            action = self.agent.act(state)
            self.snake.steer(Direction(action + 1))  # Ajustar acción a la enumeración de Direction
            self.snake.move()

            reward = 0
            if self.snake.check_collision_food(self.food):
                self.food.respawn()
                reward = 1
            if self.snake.check_collision_boundary() or self.snake.check_collision_tail():
                reward = -1
                self.snake.respawn()
                self.food.respawn()

            next_state = self.get_state()
            done = reward == -1
            self.agent.remember(state, action, reward, next_state, done)
            self.agent.replay(64)  # Tamaño de lote para el replay

            self.win.fill((0, 0, 0))
            self.snake.draw(pygame, self.win)
            self.food.draw(pygame, self.win)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = MainRL()
    game.train_agent(500)
