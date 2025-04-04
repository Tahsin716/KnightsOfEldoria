import tkinter as tk

from src.configs.grid_config import GridConfig
from src.core.simulation import Simulation


class Application:
    def __init__(self, root):
        self.root = root
        self.running = False

        self.canvas = tk.Canvas(
            root,
            width=GridConfig.GRID_SIZE * GridConfig.CELL_SIZE,
            height=GridConfig.GRID_SIZE * GridConfig.CELL_SIZE,
            bg="white"
        )
        self.canvas.grid(row=0, column=0, rowspan=6)

        self.simulation = Simulation(GridConfig.GRID_SIZE)
        self.simulation.populate()

        self.status_label = tk.Label(root, text="")
        self.status_label.grid(row=0, column=1, sticky="w")

        self.start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=1, column=1, sticky="ew")

        self.stop_button = tk.Button(root, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.grid(row=2, column=1, sticky="ew")

        self.legend_label = tk.Label(root, text=self.get_legend_text(), justify="left")
        self.legend_label.grid(row=3, column=1, sticky="nw")

    def draw_cell(self, x, y, color):
        x1 = x * GridConfig.CELL_SIZE
        y1 = y * GridConfig.CELL_SIZE
        x2 = (x + 1) * GridConfig.CELL_SIZE
        y2 = (y + 1) * GridConfig.CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def update_world(self):
        self.canvas.delete("all")
        for treasure in self.simulation.treasures:
            self.draw_cell(treasure.x, treasure.y, "yellow")
        for hideout in self.simulation.hideouts:
            self.draw_cell(hideout.x, hideout.y, "blue")
        for hunter in self.simulation.hunters:
            self.draw_cell(hunter.x, hunter.y, "green")
        for knight in self.simulation.knights:
            self.draw_cell(knight.x, knight.y, "red")

        self.update_status()
        self.simulation.step()

        if self.running and self.simulation.treasures and self.simulation.hunters:
            self.root.after(500, self.update_world)

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.update_world()

    def stop_simulation(self):
        self.running = False

    def update_status(self):
        num_hunters = len(self.simulation.hunters)
        num_knights = len(self.simulation.knights)
        num_treasures = len(self.simulation.treasures)
        total_wealth = sum([t.value for t in self.simulation.treasures])
        self.status_label.config(
            text=f"Hunters: {num_hunters} | Knights: {num_knights} | Treasures: {num_treasures} | Wealth Left: {total_wealth:.2f}"
        )

    def get_legend_text(self):
        return (
            "Legend:\n"
            "Green: Hunter\n"
            "Red: Knight\n"
            "Yellow: Treasure\n"
            "Blue: Hideout\n"
            "Gray Grid: Boundaries"
        )
