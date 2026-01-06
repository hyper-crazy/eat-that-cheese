import heapq
from collections import deque

class MazeSolvers:
    def __init__(self, grid, size, start, cheese):
        self.grid = grid
        self.size = size
        self.start = start
        self.cheese = cheese

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.grid[nx][ny] == 0:
                    neighbors.append((nx, ny))
        return neighbors

    def heuristic(self, node):
        # Manhattan Distance: |x1-x2| + |y1-y2|
        x1, y1 = node
        x2, y2 = self.cheese
        return abs(x1 - x2) + abs(y1 - y2)

    def solve_bfs(self):
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        visited_history = []
        
        while queue:
            (node, path) = queue.popleft()
            visited_history.append(node)
            if node == self.cheese:
                return {'path': path, 'history': visited_history}
            
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return {'path': [], 'history': visited_history}

    def solve_dfs(self):
        stack = [(self.start, [self.start])]
        visited = set()
        visited_history = []
        
        while stack:
            (node, path) = stack.pop()
            if node not in visited:
                visited.add(node)
                visited_history.append(node)
                if node == self.cheese:
                    return {'path': path, 'history': visited_history}
                
                for neighbor in reversed(self.get_neighbors(node)):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))
        return {'path': [], 'history': visited_history}

    # --- NEW: GREEDY BEST-FIRST SEARCH ---
    def solve_greedy(self):
        # Priority Queue stores: (Heuristic_Only, Node, Path)
        start_h = self.heuristic(self.start)
        pq = [(start_h, self.start, [self.start])]
        visited = set()
        visited_history = []
        
        while pq:
            (h, node, path) = heapq.heappop(pq)
            
            if node in visited: continue
            visited.add(node)
            visited_history.append(node)
            
            if node == self.cheese:
                return {'path': path, 'history': visited_history}
            
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    # Greedy only cares about "How close am I to the cheese?"
                    # It ignores path length.
                    priority = self.heuristic(neighbor)
                    heapq.heappush(pq, (priority, neighbor, path + [neighbor]))
        return {'path': [], 'history': visited_history}

    def solve_astar(self):
        # Priority Queue stores: (Total_Estimated_Cost, Cost_So_Far, Node, Path)
        start_h = self.heuristic(self.start)
        pq = [(start_h, 0, self.start, [self.start])]
        visited = set()
        visited_history = []
        
        while pq:
            (est_total, current_cost, node, path) = heapq.heappop(pq)
            
            if node in visited: continue
            visited.add(node)
            visited_history.append(node)
            
            if node == self.cheese:
                return {'path': path, 'history': visited_history}
            
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    new_cost = current_cost + 1
                    priority = new_cost + self.heuristic(neighbor)
                    heapq.heappush(pq, (priority, new_cost, neighbor, path + [neighbor]))
        return {'path': [], 'history': visited_history}