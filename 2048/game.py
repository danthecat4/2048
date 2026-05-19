import pygame
import numpy as np
import logic
from graphics import draw_grid
from human_agent import HumanAgent
from ai_agent_1 import AiAgent
from params import WIDTH, HEIGHT
import torch
import random
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def play_game(agent_type="ai", model_path="2048_model.pth", fps=6):
    """
    Play 2048 game with specified agent.
    
    Args:
        agent_type (str): "ai" for AI agent or "human" for human player. Default: "ai"
        model_path (str): Path to pre-trained model for AI agent. Default: "2048_model.pth"
        fps (int): Frames per second for game speed. Default: 6
    """
    pygame.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 40)
    
    grid = logic.new_grid()
    logic.spawn_tile(grid)
    logic.spawn_tile(grid)
    
    # Initialize the agent based on agent_type
    if agent_type.lower() == "human":
        agent = HumanAgent()
    elif agent_type.lower() == "ai":
        agent = AiAgent()
        if os.path.exists(model_path) and agent.net is not None:
            agent.net.load_state_dict(torch.load(model_path, map_location=device))
            print(f"Loaded trained model from {model_path}.")
        else:
            print(f"No trained model found at {model_path}. AI will use untrained network.")
        agent.epsilon = 0.0  # Disable epsilon greedy for gameplay
    else:
        raise ValueError(f"Unknown agent_type: {agent_type}. Use 'ai' or 'human'.")
    
    run = True
    while run:
        # HANDLE INPUT FROM AGENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Pass event to agent for processing (if agent supports it)
            if hasattr(agent, 'set_event'):
                agent.set_event(event)
        
        # GET ACTION FROM AGENT
        action = agent.get_action(grid, train=False)
        
        # APPLY ACTION TO LOGIC
        if action != "NONE":
            moved, reward = logic.apply_action(grid, action)
            # If move didn't change the grid, pick a random legal move
            if not moved:
                legal_moves = ["UP", "DOWN", "LEFT", "RIGHT"]
                random.shuffle(legal_moves)
                for a in legal_moves:
                    moved, reward = logic.apply_action(grid, a)
                    if moved:
                        action = a
                        break
            
            if moved:
                logic.spawn_tile(grid)
        
        if logic.is_game_over(grid):
            print(grid)
            grid = logic.reset_game()
        
        # DRAW
        draw_grid(screen, grid, font)
        
        pygame.display.update()
        clock.tick(fps)
    
    pygame.quit()


if __name__ == "__main__":
    # Play with AI agent
    play_game(agent_type="human")
