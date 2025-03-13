import tkinter as tk
from gui import BankerAlgorithmGUI

def banker_algorithm_gui():
    root = tk.Tk()
    app = BankerAlgorithmGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # Launch GUI
    banker_algorithm_gui()