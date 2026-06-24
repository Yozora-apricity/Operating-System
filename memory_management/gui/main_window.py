import tkinter as tk
from tkinter import ttk, messagebox

from models.process import Process
from models.memory_block import MemoryBlock

from mft.first_fit import FirstFit as MFTFirstFit
from mft.best_fit import BestFit as MFTBestFit
from mft.best_available_fit import BestAvailableFit

from mvt.first_fit import FirstFit as MVTFirstFit
from mvt.best_fit import BestFit as MVTBestFit
from mvt.worst_fit import WorstFit as MVTWorstFit


class MemoryGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory Management Simulator")
        self.root.geometry("1000x750")

        self.bg = "#061b33"
        self.root.configure(bg=self.bg)

        self.blocks = [
            MemoryBlock(1, 100),
            MemoryBlock(2, 200),
            MemoryBlock(3, 300),
            MemoryBlock(4, 150)
        ]

        self.create_gui()

    def create_gui(self):
        title = tk.Label(
            self.root,
            text="Memory Management Simulator",
            font=("Arial", 22, "bold"),
            bg=self.bg,
            fg="white"
        )
        title.pack(pady=10)

        controls = tk.Frame(self.root, bg=self.bg)
        controls.pack()

        tk.Label(
            controls,
            text="Total Memory:",
            bg=self.bg,
            fg="white"
        ).grid(row=0, column=0)

        self.total_memory = tk.Entry(controls)
        self.total_memory.grid(row=0, column=1)

        tk.Label(
            controls,
            text="Partitions:",
            bg=self.bg,
            fg="white"
        ).grid(row=1, column=0)

        self.partition_input = tk.Entry(controls)
        self.partition_input.grid(row=1, column=1)

        tk.Button(
            controls,
            text="CREATE MEMORY",
            command=self.create_memory,
            bg="#1976D2",
            fg="white"
        ).grid(row=2, column=1)

        tk.Label(
            controls,
            text="Process:",
            bg=self.bg,
            fg="white"
        ).grid(row=3, column=0)

        self.name = tk.Entry(controls)
        self.name.grid(row=3, column=1)

        tk.Label(
            controls,
            text="Size:",
            bg=self.bg,
            fg="white"
        ).grid(row=4, column=0)

        self.size = tk.Entry(controls)
        self.size.grid(row=4, column=1)

        # MEMORY TYPE
        tk.Label(
            controls,
            text="Memory Type:",
            bg=self.bg,
            fg="white"
        ).grid(row=5, column=0)

        self.memory_type = ttk.Combobox(
            controls,
            values=["MFT", "MVT"],
            state="readonly"
        )
        self.memory_type.current(0)
        self.memory_type.grid(row=5, column=1)
        self.memory_type.bind("<<ComboboxSelected>>", self.update_algorithms)

        # FIT TYPE
        tk.Label(
            controls,
            text="Fit Type:",
            bg=self.bg,
            fg="white"
        ).grid(row=6, column=0)

        self.algorithm = ttk.Combobox(controls, state="readonly")
        self.algorithm.grid(row=6, column=1)

        self.update_algorithms()

        # SIDE-BY-SIDE BUTTONS SUB-FRAME
        button_frame = tk.Frame(controls, bg=self.bg)
        button_frame.grid(row=7, column=0, columnspan=2, pady=15)

        tk.Button(
            button_frame,
            text="ALLOCATE",
            command=self.allocate,
            bg="#1976D2",
            fg="white",
            width=12
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="RESET",
            command=self.reset,
            bg="#1976D2",
            fg="white",
            width=12
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="EXIT",
            command=self.exit_program,
            bg="#1976D2",
            fg="white",
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        self.canvas = tk.Canvas(
            self.root,
            width=400,
            height=500,
            bg="#001933"
        )
        self.canvas.pack(pady=15)

        # STATUS DISPLAY
        self.status = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            bg=self.bg,
            fg="white"
        )
        self.status.pack(pady=5)

        self.draw_memory()

    def create_memory(self):
        try:
            total = int(self.total_memory.get())
            count = int(self.partition_input.get())

            self.blocks = []
            base = total // count
            extra = total % count

            for i in range(count):
                size = base
                if i < extra:
                    size += 1

                self.blocks.append(MemoryBlock(i + 1, size))

            self.draw_memory()

        except:
            messagebox.showerror(
                "Error",
                "Invalid memory settings"
            )

    def update_algorithms(self, event=None):
        if self.memory_type.get() == "MFT":
            self.algorithm["values"] = [
                "First Fit",
                "Best Fit",
                "Best Available Fit"
            ]
        else:
            self.algorithm["values"] = [
                "First Fit",
                "Best Fit",
                "Worst Fit"
            ]
        self.algorithm.current(0)

    def allocate(self):
        try:
            process = Process(
                self.name.get(),
                int(self.size.get())
            )
        except:
            messagebox.showerror(
                "Error",
                "Invalid process"
            )
            return  # This return is now correctly scoped INSIDE the except block

        memory = self.memory_type.get()
        fit = self.algorithm.get()

        # MFT Logic
        if memory == "MFT":
            if fit == "First Fit":
                algo = MFTFirstFit(self.blocks)
            elif fit == "Best Fit":
                algo = MFTBestFit(self.blocks)
            else:
                algo = BestAvailableFit(self.blocks)

        # MVT Logic
        else:
            if fit == "First Fit":
                algo = MVTFirstFit(self.blocks)
            elif fit == "Best Fit":
                algo = MVTBestFit(self.blocks)
            else:
                algo = MVTWorstFit(self.blocks)

        # Execution and UI updates (Now correctly inside the allocate function)
        result = algo.allocate(process)

        if result:
            messagebox.showinfo(
                "Allocated",
                f"{process.name} allocated successfully"
            )
        else:
            messagebox.showwarning(
                "Failed",
                "Not enough memory"
            )

        self.draw_memory()

    def reset(self):
        self.blocks = []
        try:
            total = int(self.total_memory.get())
            count = int(self.partition_input.get())

            base = total // count
            extra = total % count

            for i in range(count):
                size = base
                if i < extra:
                    size += 1

                self.blocks.append(MemoryBlock(i + 1, size))
        except:
            pass

        self.name.delete(0, tk.END)
        self.size.delete(0, tk.END)
        self.draw_memory()

    def exit_program(self):
        if messagebox.askyesno("Exit", "Close Simulator?"):
            self.root.destroy()

    def update_fragmentation(self):
        internal = 0
        free = 0
        used = 0

        for block in self.blocks:
            if block.process:
                used += block.process.size
                internal += (block.size - block.process.size)
            else:
                free += block.size

        external = free

        self.status.config(
            text="Memory Status\n\n"
            + f"Used Memory: {used} KB\n"
            + f"Free Memory: {free} KB\n"
            + f"Internal Fragmentation: {internal} KB\n"
            + f"External Fragmentation: {external} KB"
        )

    def draw_memory(self):
        self.canvas.delete("all")

        x = 100
        y = 40
        width = 250
        canvas_height = 430
        os_height = 35

        if len(self.blocks) == 0:
            return

        total = sum(block.size for block in self.blocks)
        scale = (canvas_height - os_height) / total
        current = y

        for block in self.blocks:
            height = block.size * scale

            # PROCESS OCCUPIED
            if block.process:
                color = "#2196F3"
                text = f"{block.process.name} - {block.process.size} KB"
            # FREE PARTITION
            else:
                color = "white"
                text = f"FREE - {block.size} KB"

            self.canvas.create_rectangle(
                x, current,
                x + width, current + height,
                fill=color,
                outline="black"
            )

            # Prevent text overflowing on very small blocks
            self.canvas.create_text(
                x + (width / 2),
                current + (height / 2),
                text=text,
                fill="black",
                font=("Arial", 9)
            )
            current += height

        # OS BLOCK
        self.canvas.create_rectangle(
            x, current,
            x + width, current + os_height,
            fill="#777777"
        )

        self.canvas.create_text(
            x + (width / 2),
            current + (os_height / 2),
            text="OS",
            fill="white"
        )

        self.update_fragmentation()

    def run(self):
        self.root.mainloop()