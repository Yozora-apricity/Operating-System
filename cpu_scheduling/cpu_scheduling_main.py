import tkinter as tk
from tkinter import messagebox

from process import Process
from scheduler_engine import SchedulerEngine
from window_header import MainWindowHeader
from left_panel import LeftControlPanel
from right_panel import RightOutputPanel

class CPUSchedulerApplication:
    """The central Controller class orchestrating the UI views and simulation engine."""
    def __init__(self, root):
        self.root = root
        self.root.title("Universal CPU Scheduling Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#E3F2FD")
        
        # Structure Parent Main Grid Configuration
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        
        # Instantiating Sub-View Component classes
        self.header = MainWindowHeader(self.root)
        self.controls = LeftControlPanel(self.root, execute_callback=self.handle_execution)
        self.output = RightOutputPanel(self.root)
        
        # Inject Default Setup Sample Data
        self.controls.add_sample_row(0, 7, 3)
        self.controls.add_sample_row(2, 4, 1)
        self.controls.add_sample_row(4, 1, 4)
        self.controls.add_sample_row(5, 4, 2)