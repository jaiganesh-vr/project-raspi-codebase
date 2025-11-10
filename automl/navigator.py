import random
from collections import deque

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
    print(f"🎯 New goal selected: {goal}")
    return goal

def load_map(filename):
    """Load matrix from a text file"""
    with open(filename) as f:
        grid = [list(map(int, line.split())) for line in f]
    return grid

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
            directions.append("reverse")  # or forward if you like
        elif r2 == r1 - 1 and c2 == c1:
            directions.append("forward")
    return directions

if __name__ == "__main__":
    grid = load_map("/Users/jaiganesh/Github/project-raspi-codebase/automl/map.txt")      
    start = (5, 5)  # top-left
    goal = generate_random_goal(grid,start)   # bottom-right

    path = find_shortest_path(grid, start, goal)
    if path:
        print("Path found:", path)
        directions = path_to_directions(path)
        print("Directions:", directions)
        start == goal
    else:
        print("No path found.")