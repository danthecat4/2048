import random
import numpy as np
from params import goaltobeat

haswon = False
# initialization
def new_grid(size=4):
    #Creates an empty grid of size squared.
    return np.zeros((size, size), dtype=int)


def spawn_tile(grid):
    #Adds a random 2 or 4 to an empty slot on the grid.
    empty = list(zip(*np.argwhere(grid == 0)))
    if not empty or len(empty[0]) == 0:
        return False
    
    idx = random.randint(0, len(empty[0]) - 1)
    r, c = empty[0][idx], empty[1][idx]
    grid[r][c] = 2 if random.random() < 0.9 else 4
    return True

# movement helpers
def compress(row):
    #Slide all numbers to the left.
    new = row[row != 0]
    new = np.append(new, np.zeros(len(row) - len(new), dtype=int))
    return new


def merge(row):
    global haswon
    #Merge equal adjacent numbers to the left.
    merged_value = 0
    for i in range(len(row) - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            merged_value += row[i]
            row[i + 1] = 0
            if row[i] >= goaltobeat:
                haswon = True
    return row, merged_value


def move_left(grid):
    moved = False
    total_reward = 0
    for r in range(len(grid)):
        original = grid[r].copy()
        row = compress(grid[r])
        row, merged_value = merge(row)
        total_reward += merged_value
        row = compress(row)
        grid[r] = row

        if not np.array_equal(row, original):
            moved = True
    return moved, total_reward


def move_right(grid):
    for r in range(len(grid)):
        grid[r].reverse()
    moved, reward = move_left(grid)
    for r in range(len(grid)):
        grid[r].reverse()
    return moved, reward


def move_up(grid):
    grid[:] = list(map(list, zip(*grid)))
    moved, reward = move_left(grid)
    grid[:] = list(map(list, zip(*grid)))
    return moved, reward


def move_down(grid):
    grid[:] = list(map(list, zip(*grid)))
    moved, reward = move_right(grid)
    grid[:] = list(map(list, zip(*grid)))
    return moved, reward

# Main interface: take action from an agent
def apply_action(grid, action):
    #Applies an action to the grid.
    #Returns (moved, reward) where moved is True if grid changed,
    #reward is 1 + sum of merged tile values for legal moves, or -5 for illegal moves.
    
    if action == "LEFT":
        moved, reward = move_left(grid)
        return moved, (1 + reward) if moved else -5
    elif action == "RIGHT":
        moved, reward = move_right(grid)
        return moved, (1 + reward) if moved else -5
    elif action == "UP":
        moved, reward = move_up(grid)
        return moved, (1 + reward) if moved else -5
    elif action == "DOWN":
        moved, reward = move_down(grid)
        return moved, (1 + reward) if moved else -5
    elif action == "NONE":
        return False, -5
    else:
        raise ValueError(f"Unknown action: {action} is not a valid action name.")
    
def is_game_over(grid):
    global haswon
    size = len(grid)
    if haswon:
        return True
    # Check for empty spaces
    if np.any(grid == 0):
        return False

    # Check for possible merges
    for r in range(size):
        for c in range(size - 1):
            if grid[r][c] == grid[r][c + 1]:
                return False
    for c in range(size):
        for r in range(size - 1):
            if grid[r][c] == grid[r + 1][c]:
                return False

    return True

def reset_game():
    global haswon
    haswon = False
    new_grid_instance = new_grid()
    spawn_tile(new_grid_instance)
    spawn_tile(new_grid_instance)
    return new_grid_instance