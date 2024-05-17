import torch
import random
from collections import deque
from model import QNet
import torch.optim as optim

class Agent:
    def __init__(self, state_size, action_size, hidden_size=64, learning_rate=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=20000)
        self.gamma = 0.99  # factor de descuento
        self.epsilon = 1.0  # tasa de exploración inicial
        self.epsilon_decay = 0.995  # decaimiento de la exploración
        self.epsilon_min = 0.01  # mínima tasa de exploración
        self.model = QNet(9, hidden_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)

    def save_model(self, file_path):
        torch.save(self.model.state_dict(), file_path)

    def load_model(self, file_path):
        self.model.load_state_dict(torch.load(file_path))
        self.model.eval()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)
        action_values = self.model(state)
        return torch.argmax(action_values).item()

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.FloatTensor(next_state).unsqueeze(0)
                target = reward + self.gamma * torch.max(self.model(next_state)).item()
            state = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.model(state)
            target_q_values = q_values.clone()
            target_q_values[0][action] = target
            loss = torch.nn.functional.mse_loss(q_values, target_q_values)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
