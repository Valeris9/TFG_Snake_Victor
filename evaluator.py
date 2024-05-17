import pygame
from food import Food
from snake import Snake, Direction
from agent import Agent


class Evaluator:
    def __init__(self, model_path, episodes=100):
        pygame.init()
        self.boundary = (800, 600)
        self.win = pygame.display.set_mode(self.boundary)
        pygame.display.set_caption("Snake Game Evaluation")

        self.block_size = 20
        self.episodes = episodes
        self.agent = Agent(11, 4)
        self.agent.load_model(model_path)

    def get_state(self, snake, food):
        head_x, head_y = snake.body[-1]
        food_x, food_y = food.x, food.y

        state = [
            head_x < food_x,  # Food to the right
            head_x > food_x,  # Food to the left
            head_y < food_y,  # Food below
            head_y > food_y,  # Food above
            head_x - self.block_size < 0,  # Danger left
            head_x + self.block_size >= self.boundary[0],  # Danger right
            head_y - self.block_size < 0,  # Danger up
            head_y + self.block_size >= self.boundary[1],  # Danger down
            snake.direction == Direction.RIGHT,
            snake.direction == Direction.LEFT,
            snake.direction == Direction.DOWN,
            snake.direction == Direction.UP
        ]
        return state

    def evaluate(self):
        total_rewards = []
        for episode in range(self.episodes):
            snake = Snake(self.block_size, self.boundary)
            food = Food(self.block_size, self.boundary)
            state = self.get_state(snake, food)
            total_reward = 0

            done = False
            while not done:
                action = self.agent.act(state)
                snake.steer(Direction(action + 1))
                snake.move()

                reward = 0
                if snake.check_collision_food(food):
                    reward = 1
                elif snake.check_collision_boundary() or snake.check_collision_tail():
                    reward = -1
                    done = True

                next_state = self.get_state(snake, food)
                state = next_state
                total_reward += reward

                # Actualizar pantalla
                self.win.fill((0, 0, 0))
                snake.draw(pygame, self.win)
                food.draw(pygame, self.win)
                pygame.display.flip()

                pygame.time.delay(50)

            total_rewards.append(total_reward)
            print(f"Episode {episode + 1}/{self.episodes} - Total Reward: {total_reward}")

        pygame.quit()
        return total_rewards


if __name__ == "__main__":
    evaluator = Evaluator(model_path="snake_model.pth", episodes=100)
    rewards = evaluator.evaluate()
    print("Evaluation Complete")
    print(f"Average Reward: {sum(rewards) / len(rewards)}")

