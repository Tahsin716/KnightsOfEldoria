import tkinter as tk

from src.configs.grid_config import GridConfig
from src.core.simulation import Simulation

class Application:
    CANVAS_ROWSPAN = 7

    def __init__(self, root):
        self.root = root
        self.simulation_running = False
        self.simulation_speed_ms = 500

        canvas_size = GridConfig.GRID_SIZE * GridConfig.CELL_SIZE
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=self.CANVAS_ROWSPAN)

        self.simulation = Simulation(GridConfig.GRID_SIZE)
        self.simulation.populate()

        self.start_button = tk.Button(root, text="Start", command=self.start_simulation)
        self.start_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_simulation)
        self.stop_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.legend_frame = tk.Frame(root)
        self.legend_frame.grid(row=2, column=1, sticky="n", padx=10)
        tk.Label(self.legend_frame, text="Legend", font=("Arial", 10, "bold")).pack(anchor="w")
        self.add_legend_item("Garrison", "black")
        self.add_legend_item("Hideout", "blue")
        self.add_legend_item("Knight", "red")
        self.add_legend_item("Hunter", "green")
        self.add_legend_item("Hunter (Carrying)", "purple")

        self.add_legend_item("Treasure (Gold)", "gold")
        self.add_legend_item("Treasure (Silver)", "silver")
        self.add_legend_item("Treasure (Bronze)", "orange")

        self.status_label = tk.Label(root, text="", justify="left", anchor="w", wraplength=180)
        self.status_label.grid(row=3, column=1, sticky="nw", padx=10)

        self.step_label = tk.Label(root, text="Step: 0")
        self.step_label.grid(row=4, column=1, sticky="nw", padx=10)

        self.update_world()

    def add_legend_item(self, text, color):
        frame = tk.Frame(self.legend_frame)
        frame.pack(anchor="w")
        try:
            color_box = tk.Label(frame, bg=color, width=2, height=1, relief="raised", borderwidth=1)
            color_box.pack(side="left", padx=(0, 5))
        except tk.TclError:
             color_box = tk.Label(frame, text="?", width=2, height=1, relief="raised", borderwidth=1)
             color_box.pack(side="left", padx=(0, 5))
        label = tk.Label(frame, text=text)
        label.pack(side="left")

    def get_text_color(self, bg_color):
        dark_colors = ["black", "blue", "red", "purple", "darkred", "maroon", "saddlebrown", "green", "darkgreen"]
        try:
             if bg_color.lower() in dark_colors:
                 return "white"
        except AttributeError:
             pass
        return "black"

    def draw_entity_with_text(self, x, y, color, display_text=""):
        size = GridConfig.CELL_SIZE
        x1, y1 = x * size, y * size
        x2, y2 = (x + 1) * size, (y + 1) * size

        try:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        except tk.TclError:
             self.canvas.create_rectangle(x1, y1, x2, y2, fill="pink", outline="gray")
             color = "pink"

        if display_text and size > 12:
            text_color = self.get_text_color(color)
            font_size = max(6, int(size * 0.35))
            try:
                self.canvas.create_text(
                    x1 + size / 2, y1 + size / 2,
                    text=display_text, fill=text_color, font=("Arial", font_size)
                )
            except tk.TclError as e:
                 print(f"Warning: Error drawing text '{display_text}': {e}")
                 try:
                     self.canvas.create_text(x1 + size / 2, y1 + size / 2, text="?", fill=text_color)
                 except tk.TclError:
                     pass


    def draw_grid_lines(self):
        size = GridConfig.CELL_SIZE
        max_coord = GridConfig.GRID_SIZE * size
        for i in range(GridConfig.GRID_SIZE + 1):
            pos = i * size
            self.canvas.create_line(pos, 0, pos, max_coord, fill="lightgray")
            self.canvas.create_line(0, pos, max_coord, pos, fill="lightgray")

    def start_simulation(self):
        if not self.simulation_running:
            self.simulation_running = True
            self.run_simulation_step()

    def stop_simulation(self):
        self.simulation_running = False

    def run_simulation_step(self):
        if self.simulation_running and not self.simulation.is_simulation_over():
            self.simulation.step()
            self.update_world()
            self.root.after(self.simulation_speed_ms, self.run_simulation_step)
        else:
            self.simulation_running = False
            self.update_world()

    def update_world(self):
        self.canvas.delete("all")
        self.draw_grid_lines()

        for garrison in self.simulation.garrisons:
            self.draw_entity_with_text(garrison.x, garrison.y, "black", "")
        for hideout in self.simulation.hideouts:
            self.draw_entity_with_text(hideout.x, hideout.y, "blue", "")

        treasure_color_map = {"GOLD": "gold", "SILVER": "silver", "BRONZE": "orange"}
        for treasure in self.simulation.treasures:
            color = treasure_color_map.get(treasure.t_type.name, "yellow")
            value_text = f"{treasure.value:.1f}"
            self.draw_entity_with_text(treasure.x, treasure.y, color, value_text)

        for knight in self.simulation.knights:
            energy_text = str(int(knight.energy))
            self.draw_entity_with_text(knight.x, knight.y, "red", energy_text)

        for hunter in self.simulation.hunters:
            color = "purple" if hunter.carrying else "green"
            stamina_text = str(int(hunter.stamina))
            self.draw_entity_with_text(hunter.x, hunter.y, color, stamina_text)

        self.display_status()
        self.step_label.config(text=f"Step: {self.simulation.simulation_step}")


    def display_status(self):
        total_value_remaining = sum(t.value for t in self.simulation.treasures)
        total_wealth_collected = sum(t.value for h in self.simulation.hideouts for t in h.stored_treasure)
        alive_hunters = sum(1 for h in self.simulation.hunters if h.stamina > 0 and not h.is_dead)
        total_knights = len(self.simulation.knights)

        status_text = (
            f"Hunters Alive: {alive_hunters}\n"
            f"Knights: {total_knights}\n"
            f"Treasures Left: {len(self.simulation.treasures)}\n"
            f"Value Remaining: {total_value_remaining:.2f}\n"
            f"Wealth Collected: {total_wealth_collected:.2f}"
        )
        if self.simulation.knights:
             avg_knight_energy = sum(k.energy for k in self.simulation.knights) / len(self.simulation.knights)
             status_text += f"\nAvg Knight Energy: {avg_knight_energy:.1f}"

        self.status_label.config(text=status_text)