import random
from collections import deque

class MazeGenerator:
    def __init__(self, size, start, cheese):
        self.size = size
        self.start = start
        self.cheese = cheese
        self.grid = []

    def generate(self):
        """Creates a grid with walls and ensures a path exists."""
        # 0 = Empty, 1 = Wall
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        # Add random walls (approx 30% density)
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) != self.start and (r, c) != self.cheese:
                    if random.random() < 0.3:
                        self.grid[r][c] = 1

        # Ensure solvability
        if not self._check_path_exists():
            self._force_path()
        
        return self.grid

    def _check_path_exists(self):
        """BFS to check connectivity."""
        q = deque([self.start])
        visited = {self.start}
        while q:
            curr = q.popleft()
            if curr == self.cheese:
                return True
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = curr[0]+dx, curr[1]+dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.grid[nx][ny] == 0 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        q.append((nx, ny))
        return False

    def _force_path(self):
        """Drills a path if the random walls blocked the cheese."""
        cx, cy = self.start
        target_x, target_y = self.cheese
        while (cx, cy) != (target_x, target_y):
            self.grid[cx][cy] = 0 
            if cx < target_x: cx += 1
            elif cx > target_x: cx -= 1
            elif cy < target_y: cy += 1
            elif cy > target_y: cy -= 1
        self.grid[target_x][target_y] = 0