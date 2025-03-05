import tkinter as tk
import heapq
import time

# Grid configuration
GRID_SIZE = 20   # 20x20 grid
CELL_SIZE = 30   # Each cell is 30 pixels

# Colors
COLOR_EMPTY = "white"
COLOR_OBSTACLE = "black"
COLOR_START = "green"
COLOR_END = "red"
COLOR_PATH = "yellow"
COLOR_EXPLORED = "lightblue"

# Initialize the window
root = tk.Tk()
root.title("Pathfinding Visualizer")

# Create the grid UI
canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.pack()

# Grid data structure
grid = [["empty" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Track start and end points
start = None
end = None

# Function to draw the grid
def draw_grid():
    canvas.delete("all")  # Clear previous grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x1, y1 = col * CELL_SIZE, row * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            color = COLOR_EMPTY
            if grid[row][col] == "obstacle":
                color = COLOR_OBSTACLE
            elif grid[row][col] == "start":
                color = COLOR_START
            elif grid[row][col] == "end":
                color = COLOR_END
            elif grid[row][col] == "path":
                color = COLOR_PATH
            elif grid[row][col] == "explored":
                color = COLOR_EXPLORED
            canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=color, tags=f"cell_{row}_{col}")

# Function to handle mouse clicks
def handle_click(event):
    global start, end
    col, row = event.x // CELL_SIZE, event.y // CELL_SIZE
    
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        if start is None:  # Set start position
            start = (row, col)
            grid[row][col] = "start"
        elif end is None:  # Set end position
            end = (row, col)
            grid[row][col] = "end"
        else:  # Set obstacles
            if grid[row][col] == "empty":
                grid[row][col] = "obstacle"
            else:
                grid[row][col] = "empty"  # Remove obstacle
        draw_grid()

# A* Pathfinding Algorithm
def a_star():
    if start is None or end is None:
        return

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan Distance

    open_set = []
    heapq.heappush(open_set, (0, start))  # (cost, position)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:  # Path found
            reconstruct_path(came_from, current)
            return

        neighbors = get_neighbors(current)

        for neighbor in neighbors:
            if grid[neighbor[0]][neighbor[1]] == "obstacle":
                continue  # Skip obstacles

            temp_g_score = g_score[current] + 1

            if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                grid[neighbor[0]][neighbor[1]] = "explored"
                draw_grid()
                time.sleep(0.05)  # Slow down visualization
                root.update()

# Get neighbors (up, down, left, right)
def get_neighbors(pos):
    row, col = pos
    neighbors = []
    if row > 0: neighbors.append((row - 1, col))  # Up
    if row < GRID_SIZE - 1: neighbors.append((row + 1, col))  # Down
    if col > 0: neighbors.append((row, col - 1))  # Left
    if col < GRID_SIZE - 1: neighbors.append((row, col + 1))  # Right
    return neighbors

# Reconstruct and draw the path
def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        if current != start:
            grid[current[0]][current[1]] = "path"
        draw_grid()
        time.sleep(0.05)  # Slow down visualization
        root.update()

# Reset the grid
def reset_grid():
    global start, end
    start = None
    end = None
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = "empty"
    draw_grid()

# UI Buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

start_button = tk.Button(btn_frame, text="Start Pathfinding", command=a_star)
start_button.pack(side=tk.LEFT, padx=10, pady=10)

reset_button = tk.Button(btn_frame, text="Reset", command=reset_grid)
reset_button.pack(side=tk.LEFT, padx=10, pady=10)

# Bind events
canvas.bind("<Button-1>", handle_click)

# Draw initial grid
draw_grid()

# Run the Tkinter event loop
root.mainloop()
