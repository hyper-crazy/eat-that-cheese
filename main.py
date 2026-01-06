import tkinter as tk
from ui.gui import AppWindow

if __name__ == "__main__":
    root = tk.Tk()
    app = AppWindow(root)
    root.mainloop()