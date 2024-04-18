import torch
import random
import numpy as np
from model import Qlearner, QTrainer
from printer import plot
from snake_environment import SnakeEnvironment
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class SnakeAgent:
    def __init__(self,environment):
        self.environment = environment
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Qlearner(input_size=(environment.width // 20) * (environment.height // 20), hidden_size=256, output_size=3)
        self.trainer = QTrainer(model=self.model, lr=LR, gamma=self.gamma)

    def get_state(self):
        state = self.environment.get_state()
        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        states = np.array(states)
        next_states = np.array(next_states)

        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self):
        state = self.get_state()
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

    def train(self, n_episodes=1000):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0

        for episode in range(n_episodes):
            state = self.environment.reset()
            done = False
            score = 0

            while not done:
                action = self.get_action()
                next_state, reward, done = self.environment.play_step(action)
                self.remember(state, action, reward, next_state, done)
                self.train_long_memory()
                self.train_short_memory(state, action, reward, next_state, done)
                state = next_state
                score += reward

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / (episode + 1)
            plot_mean_scores.append(mean_score)

            if score > record:
                record = score
                self.model.save()

            if episode % 10 == 0:
                plot(plot_scores, plot_mean_scores)

            self.train_long_memory()

if __name__ == '__main__':
    env = SnakeEnvironment(800, 600)
    agent = SnakeAgent(env)
    agent.train()

