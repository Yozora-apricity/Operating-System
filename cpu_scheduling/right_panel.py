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