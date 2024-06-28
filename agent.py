import torch
import random
import numpy as np
from collections import deque
from snake_ai import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from printer import plot
import time

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
GAMMA = 0.9
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01
NUM_EPISODES = 200
TIME_LIMIT = 3600

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 1.0  # Inicializar con alta exploración
        self.gamma = GAMMA
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 4)
        self.model.load()  # Cargar el modelo guardado
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

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

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = max(MIN_EPSILON, self.epsilon * EPSILON_DECAY)
        final_move = [0, 0, 0, 0]
        if random.uniform(0, 1) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float).unsqueeze(0)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        #print(f"Action taken: {final_move}")
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    start_time = time.time()

    with open("results.txt", "w") as f:
        try:
            while agent.n_games < NUM_EPISODES and (time.time() - start_time) < TIME_LIMIT:
                state_old = agent.get_state(game)
                final_move = agent.get_action(state_old)
                reward, done, score = game.play_step(final_move)
                state_new = agent.get_state(game)
                agent.train_short_memory(state_old, final_move, reward, state_new, done)
                agent.remember(state_old, final_move, reward, state_new, done)

                if done:
                    game.reset()
                    agent.n_games += 1
                    agent.train_long_memory()

                    if score > record or agent.n_games % 50:
                        record = score
                        print('Model saved')
                        agent.model.save()

                    print('Game', agent.n_games, 'Score', score, 'Record:', record)
                    f.write(f'{score}\n')
                    plot_scores.append(score)
                    total_score += score
                    mean_score = total_score / agent.n_games
                    plot_mean_scores.append(mean_score)
                    plot(plot_scores, plot_mean_scores)

        except KeyboardInterrupt:
            print('Training interrupted. Saving model...')
            agent.model.save()
            print('Model saved. Exiting...')

if __name__ == '__main__':
    train()