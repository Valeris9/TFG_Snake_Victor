import torch
import numpy as np
from snake_ai import SnakeGameAI, Direction, Point
from model import Linear_QNet
import matplotlib.pyplot as plt

class Evaluator:
    def __init__(self, model_path='/model/model.pth', num_games=100):
        self.model = Linear_QNet(11, 256, 4)
        self.model.load(model_path)
        self.model.eval()  # Modo de evaluación
        self.num_games = num_games

    def get_state(self, game):
        head = game.snake.body[-1]
        point_l = Point(head[0] - game.snake.block_size, head[1])
        point_r = Point(head[0] + game.snake.block_size, head[1])
        point_u = Point(head[0], head[1] - game.snake.block_size)
        point_d = Point(head[0], head[1] + game.snake.block_size)

        dir_l = game.snake.direction == Direction.LEFT
        dir_r = game.snake.direction == Direction.RIGHT
        dir_u = game.snake.direction == Direction.UP
        dir_d = game.snake.direction == Direction.DOWN

        state = [
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            game.food.x < head[0],
            game.food.x > head[0],
            game.food.y < head[1],
            game.food.y > head[1]
        ]

        return np.array(state, dtype=int)

    def get_action(self, state):
        state0 = torch.tensor(state, dtype=torch.float).unsqueeze(0)
        with torch.no_grad():  # No calcular gradientes
            prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        final_move = [0, 0, 0, 0]
        final_move[move] = 1
        return final_move

    def evaluate(self):
        game = SnakeGameAI()
        scores = []
        for i in range(self.num_games):
            game.reset()
            while True:
                state = self.get_state(game)
                final_move = self.get_action(state)
                reward, done, score = game.play_step(final_move)
                if done:
                    scores.append(score)
                    print(f"Game {i+1} Score: {score}")
                    break

        print(f'Average Score: {np.mean(scores)}')
        print(f'Max Score: {np.max(scores)}')

        plt.plot(scores)
        plt.ylabel('Score')
        plt.xlabel('Game')
        plt.title('Model Evaluation Scores')
        plt.show()

if __name__ == "__main__":
    evaluator = Evaluator(model_path='model/model.pth', num_games=100)
    evaluator.evaluate()
