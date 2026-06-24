import tkinter as tk
from tkinter import ttk

class LeftControlPanel:
    """Handles components belonging to input Sections 1 and 2."""
    def __init__(self, parent, execute_callback):
        self.execute_callback = execute_callback
        self.process_count = 0
        self.input_rows = []

        self.panel = tk.Frame(parent, bg="#E3F2FD")
        self.panel.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.panel.rowconfigure(1, weight=1)
        self.panel.columnconfigure(0, weight=1)
        
        self.algo_options = {
            "First-Come, First-Served (FCFS)": "FCFS",
            "Shortest Job First (Non-Preemptive)": "SJF_NON_PREEMP",
            "Shortest Remaining Time First (SJF Preemptive)": "SJF_PREEMP",
            "Priority (Non-Preemptive)": "PRIORITY_NON_PREEMP",
            "Priority (Preemptive)": "PRIORITY_PREEMP",
            "Round Robin (RR)": "RR"
        }
        
        self.build_section_one()
        self.build_section_two()
        self.build_action_buttons()

    def build_section_one(self):
        self.algo_frame = tk.LabelFrame(self.panel, text=" 1. Select Scheduling Algorithm ", bg="#E3F2FD", font=('Helvetica', 10, 'bold'), fg="#0D47A1", padx=10, pady=10)
        self.algo_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.algo_frame.columnconfigure(1, weight=1)
        
        tk.Label(self.algo_frame, text="Choose Type:", bg="#E3F2FD", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.algo_var = tk.StringVar()
        self.algo_dropdown = ttk.Combobox(self.algo_frame, textvariable=self.algo_var, values=list(self.algo_options.keys()), state="readonly")
        self.algo_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.algo_dropdown.current(0)
        self.algo_dropdown.bind("<<ComboboxSelected>>", self.toggle_quantum_visibility)
        
        self.lbl_quantum = tk.Label(self.algo_frame, text="Time Quantum:", bg="#E3F2FD", font=('Helvetica', 10, 'bold'))
        self.lbl_quantum.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.quantum_entry = ttk.Entry(self.algo_frame, width=8, state="disabled")
        self.quantum_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.quantum_entry.insert(0, "2")