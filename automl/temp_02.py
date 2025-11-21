def update_map_cell(filename, location, new_value):
    """
    Update a map cell given as a tuple (x, y).

    filename: "map.txt"
    location: (x, y)  -> x=row, y=column
    new_value: usually 1 to mark an obstacle
    """
    x, y = location  # unpack tuple

    # --- Load map ---
    grid = []
    with open(filename, "r") as f:
        for line in f:
            row = [int(v) for v in line.strip().split()]
            grid.append(row)

    # --- Bounds check ---
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
        raise ValueError(f"Coordinates {location} are out of bounds.")

    # --- Update the cell ---
    grid[x][y] = new_value

    # --- Save back to file ---
    with open(filename, "w") as f:
        for row in grid:
            f.write(" ".join(str(v) for v in row) + "\n")

    return grid

update_map_cell("map.txt", (3, 2), 1)
