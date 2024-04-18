import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Qlearner(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        if len(x.shape) > 2:
            x = x.view(x.size(0), -1)
        print(x.shape)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x.squeeze()

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_path = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_path)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, actions, rewards, next_state, done):
        state = torch.tensor(state.flatten(), dtype=torch.float)
        actions = torch.tensor(actions[0], dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float)
        next_state = torch.tensor(next_state.flatten(), dtype=torch.float)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            actions = torch.unsqueeze(actions, 0)
            rewards = torch.unsqueeze(rewards, 0)
            done = (done,)

        preds = self.model(state)

        targets = preds.clone()
        targets = torch.unsqueeze(targets, dim=0)
        print("Shapes: preds:", preds.shape, "actions:", actions.shape, "targets:", targets.shape)
        for idx in range(len(done)):
            Q_new = rewards[idx]
            if not done[idx]:
                Q_new = rewards[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            targets[idx][torch.argmax(actions[idx]).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(targets, preds)
        loss.backward()

        self.optimizer.step()
