import tkinter as tk
from tkinter import ttk

class RightOutputPanel:
    """Handles components and canvas painting operations inside Section 3."""
    def __init__(self, parent):
        self.colors = ["#4D4D4D", "#5DA5DA", "#FAA43A", "#60BD68", "#F17CB0", "#B2912F", "#B276B2", "#DECF3F", "#F15854"]
        
        self.output_frame = tk.LabelFrame(parent, text=" 3. Simulation Output Timeline ", bg="#E3F2FD", font=('Helvetica', 10, 'bold'), fg="#0D47A1", padx=10, pady=10)
        self.output_frame.grid(row=1, column=1, sticky="nsew", padx=15, pady=15)
        self.output_frame.rowconfigure(0, weight=1)
        self.output_frame.columnconfigure(0, weight=1)
        
        self.out_canvas = tk.Canvas(self.output_frame, borderwidth=0, highlightthickness=0, bg="#E3F2FD")
        self.out_scroll = ttk.Scrollbar(self.output_frame, orient="vertical", command=self.out_canvas.yview)
        self.out_scroll_x = ttk.Scrollbar(self.output_frame, orient="horizontal", command=self.out_canvas.xview)
        
        self.out_container = tk.Frame(self.out_canvas, bg="#E3F2FD")
        
        self.out_canvas.configure(yscrollcommand=self.out_scroll.set, xscrollcommand=self.out_scroll_x.set)
        self.out_scroll.pack(side="right", fill="y")
        self.out_scroll_x.pack(side="bottom", fill="x")
        self.out_canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas_window = self.out_canvas.create_window((0,0), window=self.out_container, anchor="nw")
        
        self.out_container.bind("<Configure>", lambda e: self.out_canvas.configure(scrollregion=self.out_canvas.bbox("all")))
        self.out_canvas.bind("<Configure>", lambda e: self.out_canvas.itemconfig(self.canvas_window, width=e.width))

    def clear(self):
        for child in self.out_container.winfo_children():
            child.destroy()

    def render_results(self, title, processes, gantt_chart):
        section = tk.LabelFrame(self.out_container, text=f" Output Results: {title} ", bg="#121212", fg="#2196F3", font=('Helvetica', 10, 'bold'), padx=10, pady=10)
        section.pack(fill="x", expand=True, pady=10, padx=5)
        
        avg_tat = sum(p.turnaround_time for p in processes) / len(processes)
        avg_wt = sum(p.waiting_time for p in processes) / len(processes)
        
        tk.Label(section, text=f"Avg Turnaround Time: {avg_tat:.2f}ms   |   Avg Waiting Time: {avg_wt:.2f}ms", font=('Helvetica', 10, 'bold'), bg="#121212", fg="white").pack(anchor="w", pady=5)
        
        t_frame = tk.Frame(section, bg="#121212")
        t_frame.pack(fill="x", expand=True, pady=5)
        
        headers = ["PID", "Arrival Time", "Burst Time", "Priority", "Completion Time", "Turnaround Time", "Waiting Time"]
        for col_idx in range(len(headers)):
            t_frame.columnconfigure(col_idx, weight=1)

        for col_idx, h in enumerate(headers):
            tk.Label(t_frame, text=h, font=('Helvetica', 9, 'bold'), anchor="center", bg="#121212", fg="white").grid(row=0, column=col_idx, padx=4, pady=2, sticky="nsew")
            
        for row_idx, p in enumerate(sorted(processes, key=lambda x: x.pid)):
            vals = [f"P{p.pid}", p.arrival_time, p.burst_time, p.priority, p.completion_time, p.turnaround_time, p.waiting_time]
            for col_idx, val in enumerate(vals):
                tk.Label(t_frame, text=str(val), font=('Helvetica', 9), anchor="center", bg="#121212", fg="white").grid(row=row_idx+1, column=col_idx, padx=4, pady=2, sticky="nsew")

        tk.Label(section, text="Gantt Chart", font=('Helvetica', 10, 'bold', 'underline'), bg="#121212", fg="white").pack(anchor="w", pady=(15, 2))

        gantt_canvas = tk.Canvas(section, height=65, bg="#1e1e1e", borderwidth=1, relief="solid", highlightthickness=0)
        gantt_canvas.pack(fill="x", expand=True, pady=5)
        
        start_x, y_top, y_bottom, scale = 20, 8, 38, 18

        for pid, start, end in gantt_chart:
            width = (end - start) * scale
            color = "#424242" if pid == "Idle" else self.colors[int(pid) % len(self.colors)]
            gantt_canvas.create_rectangle(start_x, y_top, start_x + width, y_bottom, fill=color, outline="#ffffff", width=1)
            
            label = "IDLE" if pid == "Idle" else f"P{pid}"
            text_color = "white" if pid == "Idle" else "black"
            gantt_canvas.create_text(start_x + (width/2), (y_top + y_bottom)/2, text=label, font=('Helvetica', 9, 'bold'), fill=text_color)
            gantt_canvas.create_text(start_x, y_bottom + 14, text=str(start), font=('Helvetica', 9), fill="#e0e0e0")
            start_x += width
            
        if gantt_chart:
            gantt_canvas.create_text(start_x, y_bottom + 14, text=str(gantt_chart[-1][2]), font=('Helvetica', 9), fill="#e0e0e0")