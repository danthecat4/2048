import pygame


class Agent:
    def get_action(self, grid):
        raise NotImplementedError("Subclasses must implement get_action()")


class HumanAgent(Agent):
    #Agent that takes input from keyboard
    
    def __init__(self):
        self.last_event = None
    
    def set_event(self, event):
        #Store the current pygame event for processing
        self.last_event = event
    
    def get_action(self, grid):
        #Convert keyboard input to action string
        if self.last_event is None:
            return "NONE"
        
        action = "NONE"
        if self.last_event.type == pygame.KEYDOWN:
            if self.last_event.key == pygame.K_UP:
                action = "UP"
            elif self.last_event.key == pygame.K_DOWN:
                action = "DOWN"
            elif self.last_event.key == pygame.K_LEFT:
                action = "LEFT"
            elif self.last_event.key == pygame.K_RIGHT:
                action = "RIGHT"
        
        # Clear the event after processing so it only registers once
        self.last_event = None
        return action


#Unused:
def get_action_from_keyboard(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            return "UP"
        if event.key == pygame.K_DOWN:
            return "DOWN"
        if event.key == pygame.K_LEFT:
            return "LEFT"
        if event.key == pygame.K_RIGHT:
            return "RIGHT"

    return "NONE"
