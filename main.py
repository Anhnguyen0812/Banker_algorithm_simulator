import tkinter as tk
from gui import BankerAlgorithmGUI
from gui import DeadlockDetectionAlgorithmGUI
def banker_algorithm_gui():
    root = tk.Tk()
    app = BankerAlgorithmGUI(root)
    root.mainloop()
    
def deadlock_detection_algorithm_gui():
    root = tk.Tk()
    app = DeadlockDetectionAlgorithmGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # Launch GUI
    banker_algorithm_gui()
    #deadlock_detection_algorithm_gui()
    deadlock_detection_algorithm_gui()