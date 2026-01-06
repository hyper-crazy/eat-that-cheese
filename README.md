# 🧀 Eat That Cheese: AI Pathfinding Simulator

**Eat That Cheese** is an interactive Python application that visualizes and compares the four fundamental search algorithms in Artificial Intelligence. Watch as four agents race to find the cheese using different strategies!

![Project Screenshot](https://via.placeholder.com/800x400?text=Screenshot+Placeholder)
## 🚀 Features
* **Live Simulation:** Watch BFS, DFS, Greedy, and A* solve the same maze simultaneously.
* **Dynamic Resizing:** The UI automatically adjusts to fit any screen size or maze resolution.
* **Maze Generation:** Generates random, solvable mazes every time.
* **Performance Metrics:** Displays real-time stats including:
    * **Coverage:** Percentage of the maze searched.
    * **Path Length:** Steps taken to reach the goal.
    * **Checks:** Total nodes visited.

## 🧠 The Algorithms
| Algorithm | Type | Description |
| :--- | :--- | :--- |
| **BFS (Breadth-First)** | Uninformed | Guarantees the shortest path but checks almost every box. (The Perfectionist) |
| **DFS (Depth-First)** | Uninformed | Dives deep into paths randomly. Often produces long, winding paths. (The Gambler) |
| **Greedy Best-First** | Informed | Sprints toward the goal using heuristics. Very fast but often hits walls. (The Sprinter) |
| **A* (A-Star)** | Informed | The best of both worlds. Uses heuristics to find the shortest path efficiently. (The Professional) |

## 🛠️ Installation (Source Code)
1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/eat-that-cheese.git](https://github.com/YOUR_USERNAME/eat-that-cheese.git)
    cd eat-that-cheese
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the app:**
    ```bash
    python main.py
    ```

## 📦 Download Executable
Don't want to install Python? Download the latest `.exe` file from the [Releases Page](../../releases).

## 📝 Controls
* **Size:** Set the grid size (e.g., 10 for a 10x10 maze, 50 for a huge maze).
* **Start/Cheese X,Y:** Set custom starting and ending coordinates.
* **Run Simulation:** Generates a new maze and starts the race.

## 📜 License
This project is open-source.