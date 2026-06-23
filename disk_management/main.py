import sys
import subprocess
import importlib.util

def ensure_installed(package_name, import_name=None):
    """Checks if a package is installed, and installs it via pip if it is not."""
    if import_name is None:
        import_name = package_name
        
    if importlib.util.find_spec(import_name) is None:
        print(f"Missing library detected. Auto-installing '{package_name}'... Please wait.")
        try:
            # sys.executable ensures we use the pip attached to the current Python environment
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"Successfully installed {package_name}.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package_name}. You may need to install it manually.")
            sys.exit(1)

# AUTO-INSTALL EXECUTION
ensure_installed("PyQt6")
ensure_installed("matplotlib")

# IMPORTS AND LOGIC
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QMessageBox, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Import your separated algorithm modules
from fcfs import FCFSScheduler
from sstf import SSTFScheduler
from scan import SCANScheduler
from c_scan import CSCANScheduler
from look import LOOKScheduler
from c_look import CLOOKScheduler

class MplCanvas(FigureCanvasQTAgg):
    """A simple Matplotlib canvas to embed in the PyQt6 window."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class DiskSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disk Management Simulator")
        self.resize(900, 600)
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # --- LEFT PANEL (Controls) ---
        control_panel = QGroupBox("Simulation Controls")
        control_panel.setFixedWidth(300)
        form_layout = QFormLayout()
        
        # Inputs
        self.input_head = QLineEdit("50")
        self.input_requests = QLineEdit("82, 170, 43, 140, 24, 16, 190")
        self.input_disk_size = QLineEdit("200")
        
        # Algorithm Dropdown
        self.combo_algo = QComboBox()
        self.combo_algo.addItems(["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"])
        
        # Direction Dropdown
        self.combo_direction = QComboBox()
        self.combo_direction.addItems(["up", "down"])
        
        # Run Button & Result Label
        self.btn_run = QPushButton("Run Simulation")
        self.btn_run.setStyleSheet("background-color: #2b5797; color: white; font-weight: bold; padding: 8px;")
        self.btn_run.clicked.connect(self.run_simulation)
        
        self.label_result = QLabel("Total Head Movement: 0")
        self.label_result.setStyleSheet("font-size: 14px; font-weight: bold; color: #d32f2f;")
        
        # Add to form layout
        form_layout.addRow("Initial Head:", self.input_head)
        form_layout.addRow("Requests (comma sep):", self.input_requests)
        form_layout.addRow("Disk Size:", self.input_disk_size)
        form_layout.addRow("Algorithm:", self.combo_algo)
        form_layout.addRow("Direction (SCAN/LOOK):", self.combo_direction)
        form_layout.addRow("", self.btn_run)
        form_layout.addRow(self.label_result)
        
        control_panel.setLayout(form_layout)
        
        # --- RIGHT PANEL (Visualization) ---
        viz_panel = QGroupBox("Disk Scheduling Graph")
        viz_layout = QVBoxLayout()
        self.canvas = MplCanvas(self, width=6, height=5, dpi=100)
        viz_layout.addWidget(self.canvas)
        viz_panel.setLayout(viz_layout)
        
        # Add panels to main layout
        main_layout.addWidget(control_panel)
        main_layout.addWidget(viz_panel)
        
        # Draw initial empty graph
        self.setup_empty_graph()

    def setup_empty_graph(self):
        self.canvas.axes.clear()
        self.canvas.axes.set_title("Ready to Simulate")
        self.canvas.axes.set_xlabel("Track Number")
        self.canvas.axes.set_ylabel("Sequence Step")
        self.canvas.axes.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()

    def run_simulation(self):
        try:
            # 1. Parse Inputs safely
            head = int(self.input_head.text().strip())
            disk_size = int(self.input_disk_size.text().strip())
            req_str = self.input_requests.text().split(',')
            requests = [int(r.strip()) for r in req_str if r.strip()]
            algo = self.combo_algo.currentText()
            direction = self.combo_direction.currentText()
            
            # 2. Execute corresponding algorithm logic
            result = {}
            if algo == "FCFS":
                result = FCFSScheduler().execute(head, requests)
            elif algo == "SSTF":
                result = SSTFScheduler().execute(head, requests)
            elif algo == "SCAN":
                result = SCANScheduler(disk_size).execute(head, requests, direction)
            elif algo == "C-SCAN":
                result = CSCANScheduler(disk_size).execute(head, requests, direction)
            elif algo == "LOOK":
                result = LOOKScheduler().execute(head, requests, direction)
            elif algo == "C-LOOK":
                result = CLOOKScheduler().execute(head, requests, direction)

            sequence = result["sequence"]
            movement = result["total_movement"]
            
            # 3. Update UI Text
            self.label_result.setText(f"Total Head Movement: {movement}")
            
            # 4. Plot the results on the canvas
            self.plot_graph(sequence, disk_size, algo)

        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please ensure Head, Disk Size, and Requests contain valid numbers.")

    def plot_graph(self, sequence, disk_size, algo):
        self.canvas.axes.clear()
        
        # X-axis is the track number, Y-axis is the time/step (inverted to visually match OS textbooks)
        steps = range(len(sequence))
        
        self.canvas.axes.plot(sequence, steps, marker='o', color='#2b5797', linestyle='-', linewidth=2, markersize=6)
        
        # Format the graph
        self.canvas.axes.set_title(f"{algo} Disk Scheduling")
        self.canvas.axes.set_xlabel("Track Number")
        self.canvas.axes.set_ylabel("Sequence Step (Time)")
        self.canvas.axes.set_xlim(0, disk_size - 1)
        self.canvas.axes.set_yticks(steps)
        self.canvas.axes.invert_yaxis() # Invert Y so step 0 is at the top
        
        self.canvas.axes.grid(True, linestyle='--', alpha=0.6)
        
        # Redraw the canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiskSimulatorApp()
    window.show()
    sys.exit(app.exec())