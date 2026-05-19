import pygame
import numpy as np
import logic
from graphics import draw_grid
from human_agent import HumanAgent
from ai_agent_1 import AiAgent
from params import WIDTH, HEIGHT

pygame.init()

WIDTH, HEIGHT = WIDTH, HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 40)

grid = logic.new_grid()
logic.spawn_tile(grid)
logic.spawn_tile(grid)

# Initialize the agent (change this to use different agents)
agent = AiAgent()

def main():
    global grid
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
        action = agent.get_action(grid)

        # APPLY ACTION TO LOGIC
        if action != "NONE":
            if logic.apply_action(grid, action):
                logic.spawn_tile(grid)

        if logic.is_game_over(grid):
            print(grid)
            grid = logic.reset_game()
        
        # DRAW
        draw_grid(screen, grid, font)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
