import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
import settings
from ai.generator import MazeGenerator
from ai.solvers import MazeSolvers

class AppWindow:
    def __init__(self, root):
        self.root = root
        self.root.title(settings.WINDOW_TITLE)
        
        # --- 1. SETUP WINDOW ---
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        w = int(screen_width * 0.9)
        h = int(screen_height * 0.9)
        x = int((screen_width - w) / 2)
        y = int((screen_height - h) / 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        self.root.rowconfigure(1, weight=1) 
        self.root.columnconfigure(0, weight=1)

        # State
        self.size = 10
        self.start = (0, 0)
        self.cheese = (9, 9)
        self.grid = []
        self.animating = False
        self.cell_size = 30 
        self.has_run = False
        
        self.res_bfs = None
        self.res_dfs = None
        self.res_greedy = None
        self.res_astar = None

        self.stat_labels = {}
        self.detail_labels = {} 

        # Images
        try:
            self.raw_rat_img = Image.open(settings.PATH_RAT)
            self.raw_cheese_img = Image.open(settings.PATH_CHEESE)
        except FileNotFoundError:
            self.raw_rat_img = Image.new('RGBA', (64, 64), (255, 0, 0, 0))
            self.raw_cheese_img = Image.new('RGBA', (64, 64), (255, 255, 0, 0))

        self.tk_rat_icon = None
        self.tk_cheese_icon = None
        
        self._setup_ui()
        self.main_frame.bind('<Configure>', self._on_resize)

    def _setup_ui(self):
        # --- TOP: CONTROLS ---
        ctrl_frame = tk.Frame(self.root, padx=10, pady=10, bg="#222")
        ctrl_frame.grid(row=0, column=0, sticky="ew")
        
        lbl_style = {"bg": "#222", "fg": "white", "font": ("Arial", 10)}
        
        tk.Label(ctrl_frame, text="Size:", **lbl_style).pack(side=tk.LEFT, padx=5)
        self.ent_size = tk.Entry(ctrl_frame, width=4)
        self.ent_size.insert(0, "10")
        self.ent_size.pack(side=tk.LEFT)

        tk.Label(ctrl_frame, text=" Start X,Y:", **lbl_style).pack(side=tk.LEFT, padx=5)
        self.ent_sx = tk.Entry(ctrl_frame, width=3)
        self.ent_sx.insert(0, "0")
        self.ent_sx.pack(side=tk.LEFT)
        self.ent_sy = tk.Entry(ctrl_frame, width=3)
        self.ent_sy.insert(0, "0")
        self.ent_sy.pack(side=tk.LEFT)

        tk.Label(ctrl_frame, text=" Cheese X,Y:", **lbl_style).pack(side=tk.LEFT, padx=5)
        self.ent_cx = tk.Entry(ctrl_frame, width=3)
        self.ent_cx.insert(0, "9")
        self.ent_cx.pack(side=tk.LEFT)
        self.ent_cy = tk.Entry(ctrl_frame, width=3)
        self.ent_cy.insert(0, "9")
        self.ent_cy.pack(side=tk.LEFT)

        btn = tk.Button(ctrl_frame, text="RUN SIMULATION", command=self.run_simulation, bg=settings.COLOR_CHEESE, font=("Arial", 10, "bold"))
        btn.pack(side=tk.LEFT, padx=20)
        
        # --- INFO LABEL ---
        self.lbl_result = tk.Label(ctrl_frame, text="Ready", font=("Arial", 11, "bold"), fg="#888", bg="#222")
        self.lbl_result.pack(side=tk.LEFT, padx=10)

        # --- CENTER: MAIN GRID ---
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        self.panel_bfs = self._create_panel("BFS (Breadth First)", 0, 0, settings.COLOR_BFS, "bfs")
        self.panel_dfs = self._create_panel("DFS (Depth First)", 0, 1, settings.COLOR_DFS, "dfs")
        self.panel_greedy = self._create_panel("Greedy Best-First", 1, 0, settings.COLOR_GREEDY, "greedy")
        self.panel_astar = self._create_panel("A* (A-Star)", 1, 1, settings.COLOR_ASTAR, "astar")

    def _create_panel(self, title, row, col, color, key):
        frame = tk.Frame(self.main_frame, bg="black", bd=2, relief=tk.RIDGE)
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        tk.Label(frame, text=title, fg=color, bg="black", font=("Courier", 12, "bold")).pack(fill=tk.X)
        
        container = tk.Frame(frame, bg="black")
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container, bg="black", highlightthickness=0)
        canvas.pack(anchor=tk.CENTER)

        # Standard Stats
        stats = tk.Label(frame, text="Waiting...", fg="#aaa", bg="black", font=("Arial", 9))
        stats.pack(pady=(5,0), fill=tk.X)
        self.stat_labels[key] = stats
        
        # NEW: Bold White Coverage Stat
        detail = tk.Label(frame, text="", fg="white", bg="black", font=("Arial", 11, "bold"))
        detail.pack(pady=(0,5), fill=tk.X)
        self.detail_labels[key] = detail
        
        return canvas

    def _on_resize(self, event):
        if not self.has_run or not self.grid: return
        self._calculate_layout()
        self._redraw_all_canvases()

    def _calculate_layout(self):
        panel_w = self.panel_bfs.master.winfo_width()
        panel_h = self.panel_bfs.master.winfo_height()
        if panel_w < 50: panel_w = 400
        if panel_h < 50: panel_h = 400

        min_dim = min(panel_w, panel_h)
        self.cell_size = int((min_dim * 0.8) // self.size)
        if self.cell_size < 2: self.cell_size = 2
        self._resize_icons()

    def _redraw_all_canvases(self):
        px = self.size * self.cell_size
        panels = [
            (self.panel_bfs, self.res_bfs, settings.COLOR_BFS),
            (self.panel_dfs, self.res_dfs, settings.COLOR_DFS),
            (self.panel_greedy, self.res_greedy, settings.COLOR_GREEDY),
            (self.panel_astar, self.res_astar, settings.COLOR_ASTAR)
        ]
        for panel, res, color in panels:
            panel.config(width=px, height=px)
            panel.delete("all")
            self._draw_static_board(panel)
            if res:
                for node in res['history']: self._draw_agent_history(panel, node, color)
                self._draw_final_path_line(panel, res['path'], color)

    def run_simulation(self):
        if self.animating: return 
        try:
            try:
                self.size = int(self.ent_size.get())
                sx = int(self.ent_sx.get())
                sy = int(self.ent_sy.get())
                cx = int(self.ent_cx.get())
                cy = int(self.ent_cy.get())
            except ValueError:
                raise ValueError("Please enter valid integers.")

            if self.size < 2: self.size = 2
            if self.size > 50: self.size = 50
            
            sx = max(0, min(sx, self.size - 1))
            sy = max(0, min(sy, self.size - 1))
            cx = max(0, min(cx, self.size - 1))
            cy = max(0, min(cy, self.size - 1))
            if (sx, sy) == (cx, cy):
                cx = 0 if sx != 0 else self.size - 1
                cy = 0 if sy != 0 else self.size - 1

            self._update_entry(self.ent_size, self.size)
            self._update_entry(self.ent_sx, sx)
            self._update_entry(self.ent_sy, sy)
            self._update_entry(self.ent_cx, cx)
            self._update_entry(self.ent_cy, cy)
            self.start = (sx, sy)
            self.cheese = (cx, cy)
            
            self._calculate_layout()
            
            for key in self.detail_labels:
                self.detail_labels[key].config(text="")
            self.lbl_result.config(text="Simulating...", fg="#f4d03f")
            
            gen = MazeGenerator(self.size, self.start, self.cheese)
            self.grid = gen.generate()
            
            solver = MazeSolvers(self.grid, self.size, self.start, self.cheese)
            self.res_bfs = solver.solve_bfs()
            self.res_dfs = solver.solve_dfs()
            self.res_greedy = solver.solve_greedy()
            self.res_astar = solver.solve_astar()
            
            self.has_run = True

            px = self.size * self.cell_size
            for panel in [self.panel_bfs, self.panel_dfs, self.panel_greedy, self.panel_astar]:
                panel.config(width=px, height=px)
                panel.delete("all")
                self._draw_static_board(panel)
            
            for key in self.stat_labels:
                self.stat_labels[key].config(text="Running...")

            self.animating = True
            self.step_idx = 0
            self.max_steps = max(
                len(self.res_bfs['history']), 
                len(self.res_dfs['history']), 
                len(self.res_greedy['history']),
                len(self.res_astar['history'])
            )
            
            speed = 20
            if self.size > 10: speed = 5
            if self.size > 20: speed = 1
            
            self.root.after(speed, self._animate_step)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _update_entry(self, entry, value):
        entry.delete(0, tk.END)
        entry.insert(0, str(value))

    def _resize_icons(self):
        icon_size = int(self.cell_size * 0.8)
        if icon_size < 1: icon_size = 1
        r_resized = self.raw_rat_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        c_resized = self.raw_cheese_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        self.tk_rat_icon = ImageTk.PhotoImage(r_resized)
        self.tk_cheese_icon = ImageTk.PhotoImage(c_resized)

    def _draw_static_board(self, canvas):
        for r in range(self.size):
            for c in range(self.size):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                cx, cy = x1 + self.cell_size/2, y1 + self.cell_size/2
                color = settings.COLOR_WALL if self.grid[r][c] == 1 else settings.COLOR_EMPTY
                outline = "#333" if self.cell_size > 4 else ""
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline, width=1)
                if (r, c) == self.cheese and self.tk_cheese_icon:
                    canvas.create_image(cx, cy, image=self.tk_cheese_icon, anchor=tk.CENTER)
                if (r, c) == self.start and self.tk_rat_icon:
                     canvas.create_image(cx, cy, image=self.tk_rat_icon, anchor=tk.CENTER)

    def _draw_agent_history(self, canvas, node, color):
        if not node or node == self.start or node == self.cheese: return
        r, c = node
        x1 = c * self.cell_size
        y1 = r * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        lw = 2
        if self.cell_size > 20: lw = 3
        if self.cell_size < 10: lw = 1
        pad = 2 if self.cell_size > 10 else 0
        canvas.create_rectangle(x1+pad, y1+pad, x2-pad, y2-pad, fill="", outline=color, width=lw)

    def _draw_final_path_line(self, canvas, path, color):
        if not path or len(path) < 2: return
        coords = []
        for node in path:
            cx = node[1] * self.cell_size + self.cell_size/2
            cy = node[0] * self.cell_size + self.cell_size/2
            coords.append(cx)
            coords.append(cy)
        width = 2
        if self.cell_size > 15: width = 4
        if self.cell_size > 30: width = 6
        canvas.create_line(*coords, fill=color, width=width, arrow=tk.LAST, capstyle=tk.ROUND, joinstyle=tk.ROUND)

    def _animate_step(self):
        if not self.animating: return
        
        if self.step_idx < len(self.res_bfs['history']):
            node = self.res_bfs['history'][self.step_idx]
            self._draw_agent_history(self.panel_bfs, node, settings.COLOR_BFS)
        if self.step_idx < len(self.res_dfs['history']):
            node = self.res_dfs['history'][self.step_idx]
            self._draw_agent_history(self.panel_dfs, node, settings.COLOR_DFS)
        if self.step_idx < len(self.res_greedy['history']):
            node = self.res_greedy['history'][self.step_idx]
            self._draw_agent_history(self.panel_greedy, node, settings.COLOR_GREEDY)
        if self.step_idx < len(self.res_astar['history']):
            node = self.res_astar['history'][self.step_idx]
            self._draw_agent_history(self.panel_astar, node, settings.COLOR_ASTAR)

        self.step_idx += 1
        speed = 20
        if self.size > 10: speed = 5
        if self.size > 20: speed = 1

        if self.step_idx < self.max_steps:
            self.root.after(speed, self._animate_step)
        else:
            self.root.after(50, lambda: self._finalize_step(0))

    def _finalize_step(self, stage):
        if stage == 0:
            self._draw_final_path_line(self.panel_bfs, self.res_bfs['path'], settings.COLOR_BFS)
            self._update_stats_label("bfs", self.res_bfs)
            self.root.after(50, lambda: self._finalize_step(1))
            return
        if stage == 1:
            self._draw_final_path_line(self.panel_dfs, self.res_dfs['path'], settings.COLOR_DFS)
            self._update_stats_label("dfs", self.res_dfs)
            self.root.after(50, lambda: self._finalize_step(2))
            return
        if stage == 2:
            self._draw_final_path_line(self.panel_greedy, self.res_greedy['path'], settings.COLOR_GREEDY)
            self._update_stats_label("greedy", self.res_greedy)
            self.root.after(50, lambda: self._finalize_step(3))
            return
        if stage == 3:
            self._draw_final_path_line(self.panel_astar, self.res_astar['path'], settings.COLOR_ASTAR)
            self._update_stats_label("astar", self.res_astar)
            self.root.after(50, lambda: self._finalize_step(4))
            return
        if stage == 4:
            self._show_final_details()
            self.animating = False

    # --- CLEAN & SIMPLE COVERAGE STAT ---
    def _show_final_details(self):
        results = {
            'bfs': self.res_bfs,
            'dfs': self.res_dfs,
            'greedy': self.res_greedy,
            'astar': self.res_astar
        }
        
        total_boxes = self.size * self.size
        
        self.lbl_result.config(text="Simulation Complete", fg="#2ecc71")

        for key, res in results.items():
            if len(res['path']) <= 1:
                self.detail_labels[key].config(text="Failed", fg="red")
                continue

            my_checks = len(res['history'])
            
            # Coverage %
            coverage = (my_checks / total_boxes) * 100
            
            # Bold White Text
            # Example: "Searched: 15.0%"
            txt = f"Searched: {coverage:.1f}%"
            
            self.detail_labels[key].config(text=txt, fg="white")

    def _update_stats_label(self, key, res):
        path_len = len(res['path']) - 1 if res['path'] else 0
        checked = len(res['history'])
        self.stat_labels[key].config(text=f"Checked: {checked} | Path: {path_len}")