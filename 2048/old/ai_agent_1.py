import pygame
import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import numpy as np
from params import epsilon_start, epsilon_end, epsilon_decay

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
        self.net = AiNet()
        self.grid_size = grid_size
        #Optionally, load pretrained weights here?
        #self.net.load_state_dict(torch.load("model.pth"))

        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay

        self.net.eval()

    def get_action(self, grid):
        #grid: 2D numpy array of numbers
        if random.random() < self.epsilon:
            return random.choice(self.ACTIONS)
        
        #To be honest I have no idea how this works, but it's 12:49 AM and I feel like dying so gimmie a break
        x = torch.tensor(np.array(grid), dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        with torch.no_grad():
            logits = self.net(x)
            action_idx = torch.argmax(logits, dim=1).item()
        return self.ACTIONS[action_idx]
