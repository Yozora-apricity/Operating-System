import tkinter as tk
from tkinter import ttk, messagebox

# I-import lahat ng algorithms mula sa kabilang file
from algorithms import fifo_algorithm, lru_algorithm, optimal_algorithm, counting_algorithm

class VirtualMemoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Memory Page Replacement Visualizer")
        self.root.geometry("1150x650") 
        self.root.configure(bg="#3145e1")

        # Custom Dark Mode Styles
        self.style = ttk.Style()
        self.theme_use_setting = self.style.theme_use("clam")
        self.style.configure("TLabel", background ="#4fb3f1", foreground="#FCFBFB", font = ("Helvetica", 15))
        self.style.configure("TButton", background ="#1F2627", foreground="#FCFBFB", font = ("Helvetica", 15, "bold"))
        self.style.map("TButton", background = [("active", "#76A0EA")])

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Virtual Memory: Page Replacement", font = ("Helvetica", 16, "bold"), bg ="#3145e1", fg ="#ffffff")
        title_label.pack(pady = 15)

        # Input Frame
        input_frame = tk.Frame(self.root, bg ="#4fb3f1", bd = 2, relief=tk.GROOVE)
        input_frame.pack(pady=10, padx=20, fill=tk.X)

        # Inputs
        ttk.Label(input_frame, text="Number of Frames: ").grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")
        self.frames_entry = ttk.Entry(input_frame, width = 10)
        self.frames_entry.insert(0, "3") 
        self.frames_entry.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "w")

        ttk.Label(input_frame, text="Page Reference String (comma separated):").grid(row = 0, column = 2, padx = 10, pady = 10, sticky = "w")
        self.ref_string_entry = ttk.Entry(input_frame, width = 50)
        
        # REFERENCE NUMBERS
        self.ref_string_entry.insert(0, "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1")
        self.ref_string_entry.grid(row = 0, column = 3, padx = 10, pady = 10, sticky = "w")
        ttk.Label(input_frame, text="Algorithm:").grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "w")
        self.algo_combo = ttk.Combobox(input_frame, values=["FIFO", "Optimal", "LRU", "Counting: LFU", "Counting: MFU"], state = "readonly", width=18)
        self.algo_combo.set("FIFO")
        self.algo_combo.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = "w")

        # Simulate Button
        sim_button = ttk.Button(input_frame, text = "Simulate", command = self.run_simulation)
        sim_button.grid(row = 1, column = 3, padx = 10, pady = 10, sticky = "e")

        # Results Summary Frame
        self.summary_frame = tk.Frame(self.root, bg ="#3145e1")
        self.summary_frame.pack(pady = 10)

        self.faults_label = tk.Label(self.summary_frame, text = "Total Page Faults: -", font = ("Helvetica", 11, "bold"), bg ="#3145e1", fg ="#ff0000")
        self.faults_label.pack(side = tk.LEFT, padx = 20)

        self.hits_label = tk.Label(self.summary_frame, text = "Total Page Hits: -", font = ("Helvetica", 11, "bold"), bg ="#3145e1", fg ="#3cf218")
        self.hits_label.pack(side = tk.LEFT, padx = 20)

        # Canvas for Drawing the Boxes/Grid
        self.canvas_frame = tk.Frame(self.root, bg ="#4fb3f1")
        self.canvas_frame.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="#4fb3f1", highlightthickness=0)
        self.canvas.pack(fill = tk.BOTH, expand=True)

    def run_simulation(self):
        try:
            num_frames = int(self.frames_entry.get())
            if num_frames <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive integer for frames.")
            return

        ref_str_raw = self.ref_string_entry.get()
        if not ref_str_raw.strip():
            messagebox.showerror("Input Error", "Reference string cannot be empty.")
            return
        
        try:
            pages = [int(x.strip()) for x in ref_str_raw.split(",") if x.strip() != ""]
        except ValueError:
            messagebox.showerror("Input Error", "Reference string must contain numbers separated by commas.")
            return

        algo = self.algo_combo.get()

        # Tinanggal na ang "self." dito dahil galing na sila sa algorithms.py
        if algo == "FIFO":
            steps, faults, hits = fifo_algorithm(pages, num_frames)
        elif algo == "Optimal":
            steps, faults, hits = optimal_algorithm(pages, num_frames)
        elif algo == "LRU":
            steps, faults, hits = lru_algorithm(pages, num_frames)
        elif algo == "Counting: LFU":
            steps, faults, hits = counting_algorithm(pages, num_frames, mode = "LFU")
        elif algo == "Counting: MFU":
            steps, faults, hits = counting_algorithm(pages, num_frames, mode = "MFU")

        self.faults_label.config(text = f"Total Page Faults: {faults}")
        self.hits_label.config(text = f"Total Page Hits: {hits}")
        self.draw_grid(pages, steps, num_frames)

    def draw_grid(self, pages, steps, num_frames):
        self.canvas.delete("all")
        
        box_size = 30 
        start_x = 60
        start_y = 60
        spacing_x = 48
        spacing_y = 45

        self.canvas.create_text(start_x - 50, start_y - 30, text="Ref:", anchor = "w", fill ="#ffffff", font = ("Helvetica", 10, "bold"))
        for f in range(num_frames):
            self.canvas.create_text(start_x - 50, start_y + (f * spacing_y) + (box_size/2), text=f"F{f+1}", anchor = "w", fill="#ffffff", font = ("Helvetica", 10))
        self.canvas.create_text(start_x - 50, start_y + (num_frames * spacing_y) + 20, text = "Status:", anchor = "w", fill ="#ffffff", font = ("Helvetica", 10, "bold"))

        for col, page in enumerate(pages):
            x = start_x + (col * spacing_x)
            self.canvas.create_text(x + (box_size/2), start_y - 30, text=str(page), fill ="#ffffff", font = ("Helvetica", 11, "bold"))
            
            memory_state, is_fault = steps[col]
            
            for row in range(num_frames):
                y = start_y + (row * spacing_y)
                if row < len(memory_state):
                    val = str(memory_state[row])
                    bg_color = "#898585"
                    text_color = "#ffffff"
                    if is_fault and memory_state[row] == page:
                        bg_color = "#b23b3b"
                else:
                    val = ""
                    bg_color = "#232323"
                    text_color = "#ffffff"
                
                self.canvas.create_rectangle(x, y, x + box_size, y + box_size, fill = bg_color, outline ="#9E9B9B", width = 1)
                if val:
                    self.canvas.create_text(x + (box_size/2), y + (box_size/2), text=val, fill=text_color, font=("Helvetica", 10, "bold"))
            
            status_y = start_y + (num_frames * spacing_y) + 20
            status_text = "F" if is_fault else "H"
            status_color = "#ff4a4a" if is_fault else "#39f214"
            self.canvas.create_text(x + (box_size/2), status_y, text=status_text, fill=status_color, font=("Helvetica", 10, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualMemoryGUI(root)
    root.mainloop()