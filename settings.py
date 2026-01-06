import os
import sys

# --- EXE FIX: Helper to find assets when frozen ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WINDOW_TITLE = "AI Project: Eat That Cheese (Live Simulation)"

# Image Paths (Wrapped in resource_path)
PATH_RAT = resource_path(os.path.join("assets", "rat.png"))
PATH_CHEESE = resource_path(os.path.join("assets", "cheese.png"))

# Colors
COLOR_BG = "black"
COLOR_WALL = "#333333"
COLOR_EMPTY = "white"

COLOR_BFS = "#3498db"    # Blue
COLOR_DFS = "#2ecc71"    # Green
COLOR_GREEDY = "#e67e22" # Orange
COLOR_ASTAR = "#e74c3c"  # Red

COLOR_CHEESE = "#f4d03f"
COLOR_START = "red"