import sys
import subprocess
import time
import importlib.util
import socket
import platform

# Auto-install psutil if missing
def ensure_installed(package_name):
    if importlib.util.find_spec(package_name) is None:
        print(f"Missing library detected. Auto-installing '{package_name}'...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"Successfully installed {package_name}.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package_name}. Please install manually.")
            sys.exit(1)

ensure_installed("psutil")
import psutil

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, 
                             QGridLayout, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygonF

# --- Custom Widget for Sci-Fi Edge/Corner Design ---
class SciFiFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SciFiContainer")
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Colors tailored to the bluish theme
        bg_color = QColor("#111b2b")
        corner_color = QColor("#1a365d") # Thick mechanical corners
        accent_color = QColor("#63b3ed") # Cyan lines and crosshairs
        border_color = QColor("#2b6cb0") # Thin border
        
        width = self.width()
        height = self.height()
        
        # Fill background
        painter.fillRect(0, 0, width, height, bg_color)
        
        # Draw thin main border inset slightly
        pen = QPen(border_color, 1)
        painter.setPen(pen)
        painter.drawRect(0, 0, width - 1, height - 1)
        
        # --- Draw Thick Geometric Corners (mimicking the 2nd image) ---
        painter.setBrush(corner_color)
        painter.setPen(Qt.PenStyle.NoPen)
        
        c_len = 75  # Length of the corner piece along the edge
        thick = 20  # Thickness of the corner block
        inset = c_len - 20 # Inner angle cut
        
        # Top-Left Polygon
        tl_poly = QPolygonF([
            QPointF(0, 0), QPointF(c_len, 0), QPointF(inset, thick),
            QPointF(thick, thick), QPointF(thick, inset), QPointF(0, c_len)
        ])
        painter.drawPolygon(tl_poly)
        
        # Top-Right Polygon
        tr_poly = QPolygonF([
            QPointF(width, 0), QPointF(width - c_len, 0), QPointF(width - inset, thick),
            QPointF(width - thick, thick), QPointF(width - thick, inset), QPointF(width, c_len)
        ])
        painter.drawPolygon(tr_poly)
        
        # Bottom-Left Polygon
        bl_poly = QPolygonF([
            QPointF(0, height), QPointF(c_len, height), QPointF(inset, height - thick),
            QPointF(thick, height - thick), QPointF(thick, height - inset), QPointF(0, height - c_len)
        ])
        painter.drawPolygon(bl_poly)
        
        # Bottom-Right Polygon
        br_poly = QPolygonF([
            QPointF(width, height), QPointF(width - c_len, height), QPointF(width - inset, height - thick),
            QPointF(width - thick, height - thick), QPointF(width - thick, height - inset), QPointF(width, height - c_len)
        ])
        painter.drawPolygon(br_poly)
        
        # --- Add Corner Details (Crosshairs/Plus signs) ---
        pen = QPen(accent_color, 2)
        painter.setPen(pen)
        
        # Top Right crosshair
        tr_cx, tr_cy = width - 15, 15
        painter.drawLine(tr_cx - 4, tr_cy, tr_cx + 4, tr_cy)
        painter.drawLine(tr_cx, tr_cy - 4, tr_cx, tr_cy + 4)
        
        # Bottom Left crosshair
        bl_cx, bl_cy = 15, height - 15
        painter.drawLine(bl_cx - 4, bl_cy, bl_cx + 4, bl_cy)
        painter.drawLine(bl_cx, bl_cy - 4, bl_cx, bl_cy + 4)
        
        # Bottom Right accent dot
        br_cx, br_cy = width - 15, height - 15
        painter.drawPoint(br_cx, br_cy)
        
        # --- Add Edge Decorative Bars (Top and Bottom) ---
        pen = QPen(accent_color, 3)
        painter.setPen(pen)
        
        # Top tracking line
        painter.drawLine(width // 2 - 120, thick, width // 2 + 120, thick)
        painter.fillRect(width // 2 - 135, thick - 2, 10, 7, accent_color) # Top slider block
        
        # Bottom tracking line
        painter.drawLine(width // 2 - 180, height - thick, width // 2 + 180, height - thick)
        painter.fillRect(width // 2 - 195, height - thick - 2, 10, 7, accent_color) # Bottom slider block


class SciFiDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Algorithms Dashboard")
        self.resize(1050, 650)
        self.setStyleSheet("QMainWindow { background-color: #0d141f; }")
        
        self.last_disk_io = psutil.disk_io_counters()
        self.last_time = time.time()
        
        self.create_ui()
        
        # Real-Time Update Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_stats)
        self.timer.start(1000)

    def create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        # Reduced margins to "zoom in" and push the custom frame to the window edges
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Use our custom painted frame
        container = SciFiFrame()
        container_layout = QVBoxLayout(container)
        # Increased inner margins to keep content safely away from the heavy borders
        container_layout.setContentsMargins(45, 45, 45, 35)
        
        # --- Top Header Section ---
        header_layout = QHBoxLayout()
        
        computer_name = socket.gethostname().upper()
        device_model = f"{platform.system()} {platform.release()} [{platform.machine()}]".upper()
        
        profile_label = QLabel(f"HOST: {computer_name}\nDEVICE: {device_model}")
        profile_label.setObjectName("ProfileText")
        
        self.btn_devs = QPushButton("SEE DEVELOPERS")
        self.btn_devs.setObjectName("HeaderBtn")
        self.btn_devs.setFixedSize(140, 35)
        self.btn_devs.clicked.connect(self.toggle_view)

        header_layout.addWidget(profile_label)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_devs)
        
        # --- Middle Content Section (Stacked Widget) ---
        self.stacked_widget = QStackedWidget()
        
        # Page 1: Dashboard
        self.dashboard_page = QWidget()
        self.setup_dashboard_page()
        self.stacked_widget.addWidget(self.dashboard_page)
        
        # Page 2: Developers
        self.developers_page = QWidget()
        self.setup_developers_page()
        self.stacked_widget.addWidget(self.developers_page)
        
        # --- Bottom Footer Section ---
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        
        social_label = QLabel("MODULE DEPENDENCIES")
        social_label.setObjectName("SocialLabel")
        footer_layout.addWidget(social_label)
        
        for _ in range(4):
            social_btn = QPushButton("■")
            social_btn.setObjectName("SocialBtn")
            social_btn.setFixedSize(30, 30)
            footer_layout.addWidget(social_btn)

        # Assemble main container
        container_layout.addLayout(header_layout)
        container_layout.addWidget(self.stacked_widget)
        container_layout.addLayout(footer_layout)
        
        main_layout.addWidget(container)
        self.apply_styles()

    def setup_dashboard_page(self):
        layout = QHBoxLayout(self.dashboard_page)
        layout.setContentsMargins(0, 20, 0, 20)
        
        # Left Side: Navigation Buttons 
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(15)
        
        self.btn_cpu = QPushButton("CPU SCHEDULING")
        self.btn_mem = QPushButton("MEMORY MANAGEMENT")
        self.btn_vm = QPushButton("VIRTUAL MEMORY")
        self.btn_disk = QPushButton("DISK MANAGEMENT")
        
        for btn in [self.btn_cpu, self.btn_mem, self.btn_vm, self.btn_disk]:
            btn.setObjectName("MenuBtn")
            nav_layout.addWidget(btn)
            
        self.btn_cpu.clicked.connect(self.launch_cpu)
        self.btn_mem.clicked.connect(self.launch_mem)
        self.btn_vm.clicked.connect(self.launch_vm)
        self.btn_disk.clicked.connect(self.launch_disk)
            
        nav_layout.addStretch() 
        
        # Right Side: Scores/Status Panel 
        scores_frame = QFrame()
        scores_frame.setObjectName("ScoresFrame")
        scores_layout = QVBoxLayout(scores_frame)
        scores_layout.setSpacing(10)
        
        title_label = QLabel("SYSTEM STATUS //////////")
        title_label.setObjectName("ScoresTitle")
        scores_layout.addWidget(title_label)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        self.lbl_cpu_val = QLabel("◈ -- %")
        self.lbl_mem_val = QLabel("◎ -- MB")
        self.lbl_disk_val = QLabel("❖ -- KB/s")
        
        for lbl in [self.lbl_cpu_val, self.lbl_mem_val, self.lbl_disk_val]:
            lbl.setObjectName("ScoreValueBox")
            
        lbl_cpu = QLabel("CPU LOAD")
        lbl_cpu.setObjectName("ScoreLabel")
        grid_layout.addWidget(lbl_cpu, 0, 0)
        grid_layout.addWidget(self.lbl_cpu_val, 1, 0)
        
        lbl_mem = QLabel("MEM USAGE")
        lbl_mem.setObjectName("ScoreLabel")
        grid_layout.addWidget(lbl_mem, 2, 0)
        grid_layout.addWidget(self.lbl_mem_val, 3, 0)
        
        lbl_disk = QLabel("DISK I/O")
        lbl_disk.setObjectName("ScoreLabel")
        grid_layout.addWidget(lbl_disk, 4, 0)
        grid_layout.addWidget(self.lbl_disk_val, 5, 0)
            
        scores_layout.addLayout(grid_layout)
        
        total_frame = QFrame()
        total_frame.setObjectName("TotalFrame")
        total_layout = QHBoxLayout(total_frame)
        
        total_text = QLabel("Active Processes:")
        total_text.setObjectName("TotalText")
        
        self.lbl_procs_val = QLabel("--")
        self.lbl_procs_val.setObjectName("TotalText")
        self.lbl_procs_val.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        total_layout.addWidget(total_text)
        total_layout.addWidget(self.lbl_procs_val)
        scores_layout.addWidget(total_frame)
        
        layout.addLayout(nav_layout)
        layout.addStretch()
        layout.addWidget(scores_frame)

    def setup_developers_page(self):
        layout = QVBoxLayout(self.developers_page)
        layout.setContentsMargins(0, 20, 0, 20)
        
        title = QLabel("SYSTEM ARCHITECTS & DEVELOPERS")
        title.setObjectName("ScoresTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Developer List
        devs_frame = QFrame()
        devs_frame.setObjectName("DevsFrame")
        devs_layout = QVBoxLayout(devs_frame)
        devs_layout.setSpacing(20)
        
        # Lead Developer Data
        dev_1_name = QLabel("GERALD TAN ROGADO")
        dev_1_name.setObjectName("DevNameText")
        dev_1_role = QLabel("Lead Systems Engineer | UI/UX Designer\nGitHub: Yozora-apricity")
        dev_1_role.setObjectName("DevRoleText")
        
        devs_layout.addWidget(dev_1_name)
        devs_layout.addWidget(dev_1_role)
        
        lbl_divider = QLabel("-----------------------------------")
        lbl_divider.setObjectName("ScoreLabel")
        devs_layout.addWidget(lbl_divider)
        
        dev_2_name = QLabel("TEAM MEMBER 2")
        dev_2_name.setObjectName("DevNameText")
        dev_2_role = QLabel("Backend Integration | Data Structures")
        dev_2_role.setObjectName("DevRoleText")
        
        devs_layout.addWidget(dev_2_name)
        devs_layout.addWidget(dev_2_role)
        
        layout.addWidget(devs_frame)
        layout.addStretch()

    def toggle_view(self):
        if self.stacked_widget.currentIndex() == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.btn_devs.setText("BACK TO DASHBOARD")
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.btn_devs.setText("SEE DEVELOPERS")

    def update_system_stats(self):
        if self.stacked_widget.currentIndex() != 0:
            return
            
        cpu_usage = psutil.cpu_percent(interval=None)
        self.lbl_cpu_val.setText(f"◈ {cpu_usage:.1f} %")
        
        mem = psutil.virtual_memory()
        mem_mb = mem.used / (1024 * 1024)
        self.lbl_mem_val.setText(f"◎ {mem_mb:,.0f} MB")
        
        current_disk_io = psutil.disk_io_counters()
        current_time = time.time()
        
        if self.last_disk_io and current_disk_io:
            dt = current_time - self.last_time
            d_read = current_disk_io.read_bytes - self.last_disk_io.read_bytes
            d_write = current_disk_io.write_bytes - self.last_disk_io.write_bytes
            total_kb_s = ((d_read + d_write) / 1024) / dt if dt > 0 else 0
            self.lbl_disk_val.setText(f"❖ {total_kb_s:,.0f} KB/s")
            
        self.last_disk_io = current_disk_io
        self.last_time = current_time
        
        num_procs = len(psutil.pids())
        self.lbl_procs_val.setText(f"{num_procs:,}")

    def launch_cpu(self):
        print("Launching CPU Scheduling...")
        try:
            subprocess.Popen([sys.executable, "cpu_scheduling/cpu_scheduling_main.py"])
        except Exception as e:
            print(f"Error launching CPU Scheduling: {e}")

    def launch_mem(self):
        print("Launching Memory Management...")

    def launch_vm(self):
        print("Launching Virtual Memory...")
        try:
            subprocess.Popen([sys.executable, "virtual_memory/main.py"])
        except Exception as e:
            print(f"Error launching Virtual Memory: {e}")

    def launch_disk(self):
        print("Launching Disk Management...")
        try:
            subprocess.Popen([sys.executable, "disk_management/main.py"])
        except Exception as e:
            print(f"Error launching Disk Management: {e}")

    def apply_styles(self):
        qss = """
            * {
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QLabel#ProfileText {
                color: #90cdf4;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton#HeaderBtn {
                background-color: #1a365d;
                border: 1px solid #4299e1;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
                color: #ebf8ff;
            }
            QPushButton#HeaderBtn:hover {
                background-color: #2b6cb0;
            }
            QPushButton#MenuBtn {
                background-color: #111b2b;
                border: 2px solid #2b6cb0;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                color: #63b3ed;
                min-width: 200px;
                text-align: center;
            }
            QPushButton#MenuBtn:hover {
                background-color: #2b6cb0;
                color: #ffffff;
            }
            QFrame#ScoresFrame, QFrame#DevsFrame {
                border: 1px solid #2b6cb0;
                border-radius: 6px;
                background-color: #0b1421;
                min-width: 260px;
                padding: 15px;
            }
            QLabel#ScoresTitle {
                font-size: 16px;
                font-weight: bold;
                color: #90cdf4;
                margin-bottom: 10px;
            }
            QLabel#ScoreLabel {
                font-size: 10px;
                font-weight: bold;
                color: #a0aec0;
                margin-top: 5px;
            }
            QLabel#ScoreValueBox {
                border: 1px solid #2b6cb0;
                padding: 6px;
                font-size: 12px;
                font-weight: bold;
                color: #ebf8ff;
                background-color: #1a365d;
            }
            QFrame#TotalFrame {
                background-color: #2b6cb0;
                margin-top: 10px;
                border-radius: 4px;
                padding: 5px;
            }
            QLabel#TotalText {
                color: #ffffff;
                font-weight: bold;
                font-size: 13px;
            }
            QLabel#SocialLabel {
                font-size: 10px;
                font-weight: bold;
                color: #90cdf4;
                margin-right: 10px;
            }
            QPushButton#SocialBtn {
                background-color: transparent;
                border: 1px solid #2b6cb0;
                border-radius: 4px;
                color: #63b3ed;
            }
            QPushButton#SocialBtn:hover {
                background-color: #2b6cb0;
                color: #ffffff;
            }
            QLabel#DevNameText {
                font-size: 18px;
                font-weight: bold;
                color: #ebf8ff;
            }
            QLabel#DevRoleText {
                font-size: 12px;
                color: #63b3ed;
                padding-bottom: 10px;
            }
        """
        self.setStyleSheet(qss)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SciFiDashboard()
    window.show()
    sys.exit(app.exec())