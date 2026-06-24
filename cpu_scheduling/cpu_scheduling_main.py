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

    def handle_execution(self):
        selected_algo_title = self.controls.algo_var.get()
        algo_key = self.controls.algo_options[selected_algo_title]
        
        quantum = 0
        if algo_key == "RR":
            try:
                quantum = int(self.controls.quantum_entry.get())
                if quantum <= 0: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Time Quantum must be an integer greater than 0.")
                return

        base_processes = []
        for pid, ent_arr, ent_burst, ent_prio, _ in self.controls.input_rows:
            try:
                arr = int(ent_arr.get())
                burst = int(ent_burst.get())
                prio = int(ent_prio.get())
                if arr < 0 or burst <= 0: raise ValueError
                base_processes.append(Process(pid, arr, burst, prio))
            except ValueError:
                messagebox.showerror("Error", f"Invalid entries on Process P{pid}.\nArrival must be >= 0 and Burst must be > 0.")
                return
                
        if not base_processes:
            messagebox.showwarning("Warning", "Please add at least one process row.")
            return

        self.output.clear()

        calculated_processes, gantt_chart = SchedulerEngine.simulate(base_processes, algo_key, quantum)
        self.output.render_results(selected_algo_title, calculated_processes, gantt_chart)

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerApplication(root)
    root.mainloop()