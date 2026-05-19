import pygame
import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import numpy as np
from params import epsilon_start, epsilon_end, epsilon_decay
from replaybuffer import ReplayBuffer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Agent:
    def get_action(self, grid):
        raise NotImplementedError("Subclasses must implement get_action()")


class AiNet(nn.Module):
    #Convolutional NN to decide action from grid
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 4 * 4, 64)
        self.fc2 = nn.Linear(64, 4)  #Outputs are: UP, DOWN, LEFT, RIGHT

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.flatten(start_dim=1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class AiAgent(Agent):
    #AI agent using a neural network to choose actions
    ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

    def __init__(self, grid_size = 4):
        #grid_size: assume square grid (e.g., 5 for 5x5 grid)
        self.net = AiNet().to(device)
        self.target_net = AiNet().to(device)
        self.grid_size = grid_size

        #next, some magic stuff that somehow works, I roughly understand it but like eh.
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=0.0001)

        self.gamma = 0.99
        self.batch_size = 64
        self.memory = ReplayBuffer()
        self.target_update = 1000
        self.train_steps = 0

        #Optionally, load pretrained weights here?
        #self.net.load_state_dict(torch.load("2048_model.pth"))
        #self.target_net.load_state_dict(self.net.state_dict())
        self.target_net.load_state_dict(self.net.state_dict())
        self.target_net.eval()

        #now epsilon greedy stuff, this one I actually fully understand though huh.
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay

        self.net.eval()

    def get_action(self, grid, train = True):
        #grid: 2D numpy array of numbers
        
        if train and random.random() < self.epsilon:
            return random.choice(self.ACTIONS)
        
        #To be honest I have no idea how this works, but it's 12:49 AM and I feel like dying so gimmie a break
        x = self.preprocess(grid)
        with torch.no_grad():
            logits = self.net(x)
            action_idx = torch.argmax(logits, dim=1).item()
        return self.ACTIONS[action_idx]

    def preprocess(self, grid):
        grid = np.array(grid, dtype=np.float32)
        grid = grid.copy()  # avoid modifying original
        non_zero = grid > 0
        grid[non_zero] = np.log2(grid[non_zero])
        grid[~non_zero] = 0
        return torch.tensor(grid, dtype=torch.float32, device=device).unsqueeze(0).unsqueeze(0)
    
    def action_to_index(self, action):
        return self.ACTIONS.index(action)
    
    def train_step(self):
        if len(self.memory) < self.batch_size:
            return

        self.net.train()

        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

        states = torch.cat(states)
        next_states = torch.cat(next_states)

        actions = torch.tensor(actions, device=device)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=device)
        dones = torch.tensor(dones, dtype=torch.float32, device=device)

        q_values = self.net(states)
        q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze()

        with torch.no_grad():
            next_q = self.target_net(next_states).max(1)[0]

        target = rewards + self.gamma * next_q * (1 - dones)

        loss = F.mse_loss(q_values, target)

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.net.parameters(), 1.0)
        self.optimizer.step()

        self.train_steps += 1
        if self.train_steps % self.target_update == 0:
            self.target_net.load_state_dict(self.net.state_dict())

        self.net.eval()

        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)