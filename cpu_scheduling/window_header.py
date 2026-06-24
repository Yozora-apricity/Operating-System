import tkinter as tk

class MainWindowHeader:
    """Encapsulates the Top Centered Dark Blue Banner element."""
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#0D47A1", height=55)
        self.frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.frame.grid_propagate(False)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        self.lbl_title = tk.Label(
            self.frame, 
            text="Universal CPU Scheduling Simulator", 
            font=('Helvetica', 16, 'bold'), 
            fg="white", 
            bg="#0D47A1"
        )
        self.lbl_title.grid(row=0, column=0)