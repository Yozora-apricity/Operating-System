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

    def build_section_two(self):
        self.control_frame = tk.LabelFrame(self.panel, text=" 2. Input Values for Pn ", bg="#E3F2FD", font=('Helvetica', 10, 'bold'), fg="#0D47A1", padx=10, pady=10)
        self.control_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        self.control_frame.rowconfigure(0, weight=1)
        self.control_frame.columnconfigure(0, weight=1)
        
        self.table_canvas = tk.Canvas(self.control_frame, borderwidth=0, highlightthickness=0, bg="#E3F2FD")
        self.table_frame = tk.Frame(self.table_canvas, bg="#E3F2FD")
        scrollbar = ttk.Scrollbar(self.control_frame, orient="vertical", command=self.table_canvas.yview)
        self.table_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.table_canvas.pack(side="left", fill="both", expand=True)
        self.table_canvas.create_window((0,0), window=self.table_frame, anchor="nw")
        self.table_frame.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))
        
        for c in range(4):
            self.table_frame.columnconfigure(c, weight=1)
            
        tk.Label(self.table_frame, text="PID", font=('Helvetica', 10, 'bold'), bg="#E3F2FD").grid(row=0, column=0, padx=5, pady=2)
        tk.Label(self.table_frame, text="Arrival Time", font=('Helvetica', 10, 'bold'), bg="#E3F2FD").grid(row=0, column=1, padx=5, pady=2)
        tk.Label(self.table_frame, text="Burst Time", font=('Helvetica', 10, 'bold'), bg="#E3F2FD").grid(row=0, column=2, padx=5, pady=2)
        tk.Label(self.table_frame, text="Priority", font=('Helvetica', 10, 'bold'), bg="#E3F2FD").grid(row=0, column=3, padx=5, pady=2)