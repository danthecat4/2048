import torch
import logic
from ai_agent_1 import AiAgent
import random
import wandb
from params import epsilon_start, epsilon_end, epsilon_decay, wandb_key, wandb_project


def train_agent(episodes=50000, model_save_path="2048_model.pth", log_interval=10, save_interval=1000):
    """
    Train the 2048 AI agent.
    
    Args:
        episodes (int): Number of training episodes. Default: 50000
        model_save_path (str): Path where model will be saved. Default: "2048_model.pth"
        log_interval (int): Log results every N episodes. Default: 10
        save_interval (int): Save model every N episodes. Default: 1000
    """
    agent = AiAgent()
    
    wandb.login(key=wandb_key)
    wandb.init(project=wandb_project)
    
    for episode in range(episodes):
        grid = logic.reset_game()
        
        done = False
        total_reward = 0
        step = 0
        while not done:
            step += 1
            print(step, end="\r")
            state = agent.preprocess(grid)
            
            action = agent.get_action(grid)
            
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
            
            done = logic.is_game_over(grid)
            
            next_state = agent.preprocess(grid)
            
            agent.memory.push(
                state,
                agent.action_to_index(action),
                reward,
                next_state,
                done
            )
            
            agent.train_step()
            
            total_reward += reward
        
        if episode % log_interval == 0:
            print(f"Episode {episode} | Reward: {total_reward} | Epsilon: {agent.epsilon:.3f} | Steps: {step}")
            wandb.log({"reward": total_reward, "epsilon": agent.epsilon, "steps": step}, step=episode)
        
        if episode % save_interval == 0:
            torch.save(agent.net.state_dict(), model_save_path)
            print(f"Model saved to {model_save_path}.")
    
    wandb.finish()


if __name__ == "__main__":
    train_agent()