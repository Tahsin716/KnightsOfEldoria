import tkinter as tk

from src.core.application import Application

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Eldoria Simulation")
    app = Application(root)
    root.mainloop()