import sys
import os
import subprocess
import importlib.util
import math

def ensure_installed(package_name, import_name=None):
    """Checks if a package is installed, and installs it via pip if it is not."""
    if import_name is None:
        import_name = package_name
        
    if importlib.util.find_spec(import_name) is None:
        print(f"Missing library detected. Auto-installing '{package_name}'... Please wait.")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"Successfully installed {package_name}.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package_name}. You may need to install it manually.")
            sys.exit(1)

def get_resource_path(exe_filename, dev_relative_path):
    """Safely gets the icon path for both VS Code testing and the final .exe"""
    try:
        # If running as a PyInstaller .exe, the icon gets bundled directly into the root temp folder
        base_path = sys._MEIPASS
        return os.path.join(base_path, exe_filename)
    except Exception:
        # If running in VS Code, anchor the path to THIS script's location so terminal CWD doesn't break it
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(script_dir, dev_relative_path))

# AUTO-INSTALL EXECUTION
ensure_installed("PyQt6")
ensure_installed("matplotlib")

# ORIGINAL IMPORTS AND LOGIC
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QMessageBox, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Import separated algorithm modules
from fcfs import FCFSScheduler
from sstf import SSTFScheduler
from scan import SCANScheduler
from c_scan import CSCANScheduler
from look import LOOKScheduler
from c_look import CLOOKScheduler

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#0d1117')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#0d1117')
        super(MplCanvas, self).__init__(self.fig)

class DiskSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disk Management Simulator | Pro")
        self.resize(1100, 700)
        
        # WINDOW ICON
        icon_path = get_resource_path("icon.ico", "../assets/icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Warning: Could not find icon at {icon_path}")
        
        # UI/UX THEME (QSS)
        modern_qss = """
        QMainWindow { background-color: #0d1117; }
        
        QGroupBox { 
            color: #c9d1d9; 
            border: 1px solid #30363d; 
            border-radius: 8px; 
            margin-top: 20px; 
            padding-top: 15px; 
            font-weight: 600; 
            font-family: 'Segoe UI', sans-serif; 
            font-size: 14px; 
        }
        
        QGroupBox::title { 
            subcontrol-origin: margin; 
            subcontrol-position: top left; 
            left: 15px; 
            top: 0px; 
            background-color: #0d1117; 
            padding: 0 8px; 
        }
        
        QLabel { color: #8b949e; font-family: 'Segoe UI', sans-serif; font-size: 13px; }
        
        QLineEdit, QComboBox { 
            background-color: #161b22; 
            color: #c9d1d9; 
            border: 1px solid #30363d; 
            border-radius: 6px; 
            padding: 8px; 
            font-family: 'Segoe UI', sans-serif; 
            font-size: 13px; 
            selection-background-color: #1f6feb; 
        }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #58a6ff; }
        
        QPushButton { 
            background-color: #238636; 
            color: white; 
            border: none; 
            border-radius: 6px; 
            padding: 12px; 
            font-weight: bold; 
            font-family: 'Segoe UI', sans-serif; 
            font-size: 14px; 
        }
        QPushButton:hover { background-color: #2ea043; }
        QPushButton:disabled { background-color: #21262d; color: #484f58; }
        """
        self.setStyleSheet(modern_qss)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(25)
        
        # --- LEFT PANEL (Controls) ---
        control_panel = QGroupBox("Simulation Parameters")
        control_panel.setFixedWidth(320)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        self.input_head = QLineEdit("50")
        self.input_requests = QLineEdit("82, 170, 43, 140, 24, 16, 190")
        self.input_disk_size = QLineEdit("200")
        
        self.combo_algo = QComboBox()
        self.combo_algo.addItems(["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"])
        
        self.label_direction = QLabel("Direction:")
        self.combo_direction = QComboBox()
        self.combo_direction.addItem("Increasing Track (Right)", "up")
        self.combo_direction.addItem("Decreasing Track (Left)", "down")
        
        self.combo_algo.currentTextChanged.connect(self.update_direction_ui)
        self.update_direction_ui(self.combo_algo.currentText())
        
        self.btn_run = QPushButton("Execute Simulation")
        self.btn_run.clicked.connect(self.run_simulation)
        
        self.label_result = QLabel("Total Head Movement: 0")
        self.label_result.setStyleSheet("font-size: 15px; font-weight: bold; color: #58a6ff; margin-top: 10px;")
        
        form_layout.addRow("Initial Head:", self.input_head)
        form_layout.addRow("Requests (CSV):", self.input_requests)
        form_layout.addRow("Disk Capacity:", self.input_disk_size)
        form_layout.addRow("Algorithm:", self.combo_algo)
        form_layout.addRow(self.label_direction, self.combo_direction)
        form_layout.addRow("", self.btn_run)
        form_layout.addRow(self.label_result)
        
        control_panel.setLayout(form_layout)
        
        # RIGHT PANEL (Interactive Visualization)
        viz_panel = QGroupBox("Live Scheduling Path")
        viz_layout = QVBoxLayout()
        
        self.canvas = MplCanvas(self, width=6, height=5, dpi=100)
        viz_layout.addWidget(self.canvas)
        viz_panel.setLayout(viz_layout)
        
        main_layout.addWidget(control_panel)
        main_layout.addWidget(viz_panel)
        
        # ANIMATION VARIABLES
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.sequence = []
        self.current_step = 0
        self.anim_progress = 0.0  
        self.x_data = []
        self.y_data = []
        
        # HOVER TOOLTIP SETUP
        self.annot = self.canvas.axes.annotate(
            "", xy=(0,0), xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round4,pad=0.5", fc="#161b22", ec="#58a6ff", lw=1),
            color="#ffffff", fontweight='bold', zorder=10
        )
        self.annot.set_visible(False)
        self.canvas.mpl_connect("motion_notify_event", self.hover_event)
        
        self.setup_empty_graph()

    def update_direction_ui(self, selected_algo):
        """Hides the direction dropdown completely for FCFS and SSTF."""
        if selected_algo in ["FCFS", "SSTF"]:
            self.label_direction.hide()
            self.combo_direction.hide()
        else:
            self.label_direction.show()
            self.combo_direction.show()

    def apply_dark_theme_to_axes(self):
        self.canvas.axes.tick_params(colors='#8b949e', labelsize=9)
        self.canvas.axes.xaxis.label.set_color('#8b949e')
        self.canvas.axes.yaxis.label.set_color('#8b949e')
        self.canvas.axes.title.set_color('#c9d1d9')
        self.canvas.axes.title.set_fontsize(12)
        self.canvas.axes.title.set_fontweight('bold')
        
        self.canvas.axes.spines['bottom'].set_color('#30363d')
        self.canvas.axes.spines['left'].set_color('#30363d')
        self.canvas.axes.spines['top'].set_visible(False)
        self.canvas.axes.spines['right'].set_visible(False)

    def setup_empty_graph(self):
        self.canvas.axes.clear()
        self.canvas.axes.set_title("Ready to Simulate")
        self.canvas.axes.set_xlabel("Track Number")
        self.canvas.axes.set_ylabel("Sequence Step")
        self.apply_dark_theme_to_axes()
        self.canvas.axes.grid(True, linestyle='-', color='#21262d', alpha=0.8)
        self.canvas.draw()

    def run_simulation(self):
        try:
            head = int(self.input_head.text().strip())
            disk_size = int(self.input_disk_size.text().strip())
            req_str = self.input_requests.text().split(',')
            requests = [int(r.strip()) for r in req_str if r.strip()]
            algo = self.combo_algo.currentText()
            direction = self.combo_direction.currentData()
            
            # OUT OF BOUNDS VALIDATION LOGIC
            if disk_size <= 0:
                QMessageBox.warning(self, "Invalid Capacity", "Disk Capacity must be greater than 0.")
                return

            if head < 0 or head >= disk_size:
                QMessageBox.warning(self, "Out of Bounds Error", f"Initial Head ({head}) must be within the disk bounds (0 to {disk_size - 1}).")
                return

            invalid_requests = [str(r) for r in requests if r < 0 or r >= disk_size]
            if invalid_requests:
                QMessageBox.warning(self, "Out of Bounds Error", 
                                    f"The following requests exceed the disk capacity bounds (0 to {disk_size - 1}):\n{', '.join(invalid_requests)}")
                return
            # ----------------------------------------
            
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

            self.sequence = result["sequence"]
            movement = result["total_movement"]
            
            self.label_result.setText(f"Total Head Movement: {movement}")
            
            self.start_animation(disk_size, algo)

        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please ensure Head, Disk Size, and Requests contain valid numbers.")

    def start_animation(self, disk_size, algo):
        self.timer.stop()
        self.current_step = 0
        self.anim_progress = 0.0
        self.annot.set_visible(False)
        
        self.canvas.axes.clear()
        self.canvas.axes.set_title(f"{algo} Scheduling Analysis")
        self.canvas.axes.set_xlabel("Track Number")
        self.canvas.axes.set_ylabel("Time (Sequence Step)")
        
        self.canvas.axes.set_xlim(0, disk_size - 1)
        self.canvas.axes.set_ylim(len(self.sequence) - 0.5, -0.5) 
        self.canvas.axes.set_yticks(range(len(self.sequence)))
        
        unique_tracks = sorted(list(set(self.sequence)))
        self.canvas.axes.set_xticks(unique_tracks)
        self.canvas.axes.tick_params(axis='x', rotation=45)
        
        self.apply_dark_theme_to_axes()
        self.canvas.axes.grid(True, linestyle='-', color='#21262d', alpha=0.8)
        
        # Re-add annotation object since we cleared the axes
        self.annot = self.canvas.axes.annotate(
            "", xy=(0,0), xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round4,pad=0.5", fc="#161b22", ec="#58a6ff", lw=1),
            color="#ffffff", fontweight='bold', zorder=10
        )
        self.annot.set_visible(False)
        
        if len(self.sequence) > 0:
            self.x_data = [self.sequence[0]]
            self.y_data = [0]
            
            self.path_line, = self.canvas.axes.plot(self.x_data, self.y_data, color='#1f6feb', linestyle='-', linewidth=2.5, marker='o', markersize=6, markerfacecolor='#58a6ff', zorder=2)
            self.playhead, = self.canvas.axes.plot(self.x_data, self.y_data, marker='o', color='#ffffff', markersize=8, zorder=3)
            
        self.canvas.draw()
        
        self.btn_run.setEnabled(False) 
        self.btn_run.setText("Simulating...")
        self.timer.start(25)

    def update_animation(self):
        if self.current_step < len(self.sequence) - 1:
            self.anim_progress += 0.1 
            
            if self.anim_progress >= 1.0:
                self.anim_progress = 1.0
                
            start_x = self.sequence[self.current_step]
            end_x = self.sequence[self.current_step + 1]
            start_y = self.current_step
            end_y = self.current_step + 1
            
            current_x = start_x + (end_x - start_x) * self.anim_progress
            current_y = start_y + (end_y - start_y) * self.anim_progress
            
            temp_x = self.x_data + [current_x]
            temp_y = self.y_data + [current_y]
            
            self.path_line.set_data(temp_x, temp_y)
            self.playhead.set_data([current_x], [current_y])
            
            self.canvas.draw()
            
            if self.anim_progress >= 1.0:
                self.x_data.append(end_x)
                self.y_data.append(end_y)
                self.current_step += 1
                self.anim_progress = 0.0
        else:
            self.timer.stop()
            self.btn_run.setEnabled(True)
            self.btn_run.setText("Execute Simulation")

    def hover_event(self, event):
        """Displays a tooltip with Track and Step data when hovering over a node."""
        if not event.inaxes == self.canvas.axes or not self.x_data:
            if self.annot.get_visible():
                self.annot.set_visible(False)
                self.canvas.draw_idle()
            return
            
        # Only allow hover interaction when the animation is completely finished
        if self.timer.isActive():
            return

        x, y = event.xdata, event.ydata
        closest_idx = -1
        min_dist = float('inf')
        
        for i in range(len(self.x_data)):
            dx = (self.x_data[i] - x) / max(1, self.canvas.axes.get_xlim()[1])
            dy = (self.y_data[i] - y) / max(1, self.canvas.axes.get_ylim()[0])
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist < min_dist:
                min_dist = dist
                closest_idx = i

        if min_dist < 0.05:
            track = int(self.x_data[closest_idx])
            step = int(self.y_data[closest_idx])
            
            self.annot.xy = (track, step)
            self.annot.set_text(f"Track: {track}\nStep: {step}")
            self.annot.set_visible(True)
            self.canvas.draw_idle()
        else:
            if self.annot.get_visible():
                self.annot.set_visible(False)
                self.canvas.draw_idle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiskSimulatorApp()
    window.show()
    sys.exit(app.exec())