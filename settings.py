import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WINDOW_TITLE = "AI Project: Eat That Cheese (Live Simulation)"

# Image Paths
PATH_RAT = os.path.join(BASE_DIR, "assets", "rat.png")
PATH_CHEESE = os.path.join(BASE_DIR, "assets", "cheese.png")

# Dimensions
ANIMATION_SPEED_MS = 50

# Colors
COLOR_BG = "black"
COLOR_WALL = "#333333"
COLOR_EMPTY = "white"

# Algorithm Colors
COLOR_BFS = "#3498db"    # Blue
COLOR_DFS = "#2ecc71"    # Green
COLOR_GREEDY = "#e67e22" # Orange (New!)
COLOR_ASTAR = "#e74c3c"  # Red

COLOR_CHEESE = "#f4d03f"
COLOR_START = "red"