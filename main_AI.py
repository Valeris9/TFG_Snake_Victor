import torch
from agent import SnakeAgent
from snake_environment import SnakeEnvironment
from printer import plot

def train():
    env = SnakeEnvironment(440, 440)
    agent = SnakeAgent(env)
    agent.train(n_episodes=1000)
    agent.model.save_model('trained_model.pth')

def play():
    env = SnakeEnvironment(440, 440)
    agent = SnakeAgent(env)
    agent.model.load_state_dict(torch.load('trained_model.pth'))

    game_over = False
    while not game_over:
        state = agent.get_state()
        action = agent.get_action()
        next_state, reward, game_over = agent.environment.play_step(action)

        print("Reward: ", reward)
        print("Game Over: ", game_over)

if __name__ == '__main__':
    train()
    play()
