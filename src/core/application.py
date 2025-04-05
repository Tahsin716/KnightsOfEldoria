import tkinter as tk

from src.configs.grid_config import GridConfig
from src.core.simulation import Simulation

class Application:
    def __init__(self, root):
        self.root = root
        self.simulation_running = False

        canvas_size = GridConfig.GRID_SIZE * GridConfig.CELL_SIZE
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=6)

        self.simulation = Simulation(GridConfig.GRID_SIZE)
        self.simulation.populate()

        self.start_button = tk.Button(root, text="Start", command=self.start_simulation)
        self.start_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_simulation)
        self.stop_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.legend_frame = tk.Frame(root)
        self.legend_frame.grid(row=2, column=1, sticky="n")
        tk.Label(self.legend_frame, text="Legend", font=("Arial", 10, "bold")).pack(anchor="w")
        self.add_legend_item("Treasure (Gold)", "gold")
        self.add_legend_item("Treasure (Silver)", "silver")
        self.add_legend_item("Treasure (Bronze)", "orange")
        self.add_legend_item("Hideout", "blue")
        self.add_legend_item("Hunter", "green")
        self.add_legend_item("Knight", "red")
        self.add_legend_item("Garrison", "black")

        self.status_label = tk.Label(root, text="", justify="left", anchor="w")
        self.status_label.grid(row=3, column=1, sticky="nw", padx=10)

        self.update_world()

    def add_legend_item(self, text, color):
        frame = tk.Frame(self.legend_frame)
        frame.pack(anchor="w")
        color_box = tk.Label(frame, bg=color, width=2, height=1)
        color_box.pack(side="left", padx=(0, 5))
        label = tk.Label(frame, text=text)
        label.pack(side="left")

    def draw_cell(self, x, y, color):
        size = GridConfig.CELL_SIZE
        self.canvas.create_rectangle(x * size, y * size, (x+1) * size, (y+1) * size, fill=color, outline="gray")

    def draw_grid_lines(self):
        for i in range(GridConfig.GRID_SIZE + 1):
            x = i * GridConfig.CELL_SIZE
            self.canvas.create_line(x, 0, x, GridConfig.GRID_SIZE * GridConfig.CELL_SIZE, fill="lightgray")
            self.canvas.create_line(0, x, GridConfig.GRID_SIZE * GridConfig.CELL_SIZE, x, fill="lightgray")

    def start_simulation(self):
        self.simulation_running = True
        self.update_world()

    def stop_simulation(self):
        self.simulation_running = False

    def update_world(self):
        self.canvas.delete("all")
        self.draw_grid_lines()

        color_map = {"GOLD": "gold", "SILVER": "silver", "BRONZE": "orange"}
        for treasure in self.simulation.treasures:
            color = color_map.get(treasure.t_type.name, "yellow")
            self.draw_cell(treasure.x, treasure.y, color)

        for hideout in self.simulation.hideouts:
            self.draw_cell(hideout.x, hideout.y, "blue")
        for hunter in self.simulation.hunters:
            self.draw_cell(hunter.x, hunter.y, "green")
        for knight in self.simulation.knights:
            self.draw_cell(knight.x, knight.y, "red")
        for gx, gy in self.simulation.garrison_locations:
            self.draw_cell(gx, gy, "black")

        self.display_status()

        if self.simulation_running and not self.simulation.is_simulation_over():
            self.simulation.step()
            self.root.after(500, self.update_world)

    def display_status(self):
        total_wealth = sum(t.value for t in self.simulation.treasures)
        alive_hunters = sum(1 for h in self.simulation.hunters if h.stamina > 0)
        total_knights = len(self.simulation.knights)
        self.status_label.config(text=f"Hunters Alive: {alive_hunters}\nKnights: {total_knights}\nTreasures Left: {len(self.simulation.treasures)}\nTreasure Value: {total_wealth:.2f}")
