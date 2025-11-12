import random
from collections import deque

def load_map(filename):
    """Load matrix from a text file"""
    with open(filename) as f:
        grid = [list(map(int, line.split())) for line in f]
    return grid

def generate_random_goal(grid, start):
    """
    Generate a random goal position (r, c) on the grid that:
    - is not an obstacle (grid[r][c] == 0)
    - is not the start position
    """
    rows, cols = len(grid), len(grid[0])
    free_cells = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if grid[r][c] == 0 and (r, c) != start
    ]

    if not free_cells:
        raise ValueError("No valid goal positions available!")

    goal = random.choice(free_cells)
    print(f"From the location: {start}")
    print(f"New goal selected: {goal}")

    return goal

def find_shortest_path(grid, start, goal):
    """
    BFS shortest path search on grid
    start, goal = (row, col)
    Returns list of (row, col) from start to goal
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])  # (position, path_so_far)
    visited = set([start])

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == goal:
            return path  # found it!

        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:  # right, down, left, up
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                queue.append(((nr, nc), path + [(nr, nc)]))
                visited.add((nr, nc))

    return None  # no path found

def path_to_directions(path):
    """Convert list of coordinates to movement directions"""
    directions = []
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        if r2 == r1 and c2 == c1 + 1:
            directions.append("right")
        elif r2 == r1 and c2 == c1 - 1:
            directions.append("left")
        elif r2 == r1 + 1 and c2 == c1:
            directions.append("down")  # or forward if you like
        elif r2 == r1 - 1 and c2 == c1:
            directions.append("up")
    return directions


def convert_absolute_to_relative(directions, initial_facing):
    """
    Converts absolute directions (from pathfinding) into
    relative movement commands (for a robot).
    """
    # Order of directions (clockwise)
    order = ["up", "right", "down", "left"]
    facing = initial_facing
    # Robot starts facing this way
    rel_moves = []

    for d in directions:
        if d == facing:
            rel_moves.append("forward")
        else:
            # figure out rotation needed
            current_idx = order.index(facing)
            target_idx = order.index(d)
            diff = (target_idx - current_idx) % 4

            if diff == 1:
                rel_moves.append("right")
            elif diff == 3:
                rel_moves.append("left")
            elif diff == 2:
                rel_moves.append("reverse")
                        
            rel_moves.append("forward")
            facing = d  # update facing direction

    return rel_moves,facing

def simplify_actions(actions):
    """
    Simplify a list of robot actions by merging patterns:
    - forward, left, forward  -> forward left
    - forward, right, forward -> forward right
    """
    simplified = []
    i = 0

    while i < len(actions):
        if i + 2 < len(actions):
            a1, a2, a3 = actions[i], actions[i + 1], actions[i + 2]

            if a1 == "forward" and a2 == "left" and a3 == "forward":
                simplified.append("forward_left")
                i += 3
                continue
            elif a1 == "forward" and a2 == "right" and a3 == "forward":
                simplified.append("forward_right")
                i += 3
                continue
        simplified.append(actions[i])
        i += 1

    return simplified

if __name__ == "__main__":
    grid = load_map("map.txt")      
    start = (0, 1)  # top-left
    goal = generate_random_goal(grid,start)   # bottom-right

    path = find_shortest_path(grid, start, goal)
    if path:
        print("Path found:", path)
        directions = path_to_directions(path)
        relative_directions, facing = convert_absolute_to_relative(directions,facing)
        print("Directions:", directions)
        print("Relative Directions:", relative_directions,facing)
        start == goal
    else:
        print("No path found.")