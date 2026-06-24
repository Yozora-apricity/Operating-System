import sys, os, subprocess, time, importlib.util, socket, platform, random

def ensure_installed(pkg):
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure_installed("psutil")
import psutil

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, 
                             QGridLayout, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, QPointF, QEvent
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygonF, QIcon

def get_resource_path(exe_filename, dev_relative_path):
    """Safely gets the asset path for both dev testing and the final .exe"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_path, exe_filename)
    if not os.path.exists(target_path):
        target_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), dev_relative_path))
    return target_path

# --- Custom Widget for Circuit Line Separator ---
class CircuitSeparator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(20)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setPen(QPen(QColor("#2b6cb0"), 1.5))
        # Draw a technical circuit line underneath the names
        painter.drawLine(0, 10, 230, 10)
        painter.drawLine(230, 10, 240, 15)
        painter.drawLine(240, 15, 260, 15)
        
        # End Node
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#63b3ed"))
        painter.drawEllipse(QPointF(260, 15), 2.5, 2.5)

# Cursor Overlay Widget for Custom Cursor and Trail Effect
class CursorOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Allows clicks to pass through to underlying buttons
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        
        self.mouse_pos = QPointF(-100, -100)
        self.trail_points = []
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_trail)
        self.timer.start(33)
        
    def update_trail(self):
        for pt in self.trail_points:
            pt[2] -= 18 # Fade out speed
        self.trail_points = [pt for pt in self.trail_points if pt[2] > 0]
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw Animated Trail
        if len(self.trail_points) > 1:
            for i in range(1, len(self.trail_points)):
                p1, p2 = self.trail_points[i-1], self.trail_points[i]
                alpha = max(0, min(255, int(p2[2])))
                painter.setPen(QPen(QColor(255, 50, 50, alpha), 2))
                painter.drawLine(QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1]))
                
        # Draw Electric Red Cursor
        mx, my = self.mouse_pos.x(), self.mouse_pos.y()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 50, 50, 255))
        painter.drawEllipse(QPointF(mx, my), 4, 4)
        painter.setBrush(QColor(255, 200, 200, 255))
        painter.drawEllipse(QPointF(mx, my), 2, 2)
        
        painter.setPen(QPen(QColor(255, 50, 50, 200), 1))
        painter.drawLine(int(mx-8), int(my), int(mx+8), int(my))
        painter.drawLine(int(mx), int(my-8), int(mx), int(my+8))

# --- Custom Widget for Background Border Elements ---
class SciFiFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SciFiContainer")
        self.grid_spacing = 40
        self.pulses = [] 
        
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animate_circuit)
        self.anim_timer.start(33) 
        
    def animate_circuit(self):
        w, h = self.width(), self.height()
        if w == 0 or h == 0: return

        # Circuit Pulse Animation
        if random.random() < 0.15: 
            axis = random.choice(['x', 'y'])
            length = random.randint(40, 120)
            speed = random.uniform(3.0, 8.0)
            if axis == 'x':
                y = random.choice(range(0, h, self.grid_spacing))
                self.pulses.append([0, y, speed, axis, 255, length])
            else:
                x = random.choice(range(0, w, self.grid_spacing))
                self.pulses.append([x, 0, speed, axis, 255, length])

        for p in self.pulses:
            if p[3] == 'x': p[0] += p[2]
            else: p[1] += p[2]
            p[4] -= 1.5 

        # Clean dead particles
        self.pulses = [p for p in self.pulses if p[4] > 0 and p[0] < w + 150 and p[1] < h + 150]
        self.update() 
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        painter.fillRect(0, 0, w, h, QColor("#111b2b"))
        
        # --- 1. Grid ---
        grid_pen = QPen(QColor("#182942"), 1)
        painter.setPen(grid_pen)
        for x in range(0, w, self.grid_spacing): painter.drawLine(x, 0, x, h)
        for y in range(0, h, self.grid_spacing): painter.drawLine(0, y, w, y)
        
        # --- 2. Circuit Pulses ---
        for p in self.pulses:
            x, y, _, axis, alpha, length = p
            alpha_val = max(0, min(255, int(alpha)))
            
            painter.setPen(QPen(QColor(43, 108, 176, int(alpha_val * 0.5)), 2))
            if axis == 'x':
                painter.drawLine(QPointF(max(0, x - length), y), QPointF(x, y))
            else:
                painter.drawLine(QPointF(x, max(0, y - length)), QPointF(x, y))
                
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(99, 179, 237, alpha_val))
            painter.drawEllipse(QPointF(x, y), 3.5, 3.5)
            painter.setBrush(QColor(255, 255, 255, alpha_val))
            painter.drawEllipse(QPointF(x, y), 1.5, 1.5)
        
        # --- 3. Main Borders ---
        painter.setPen(QPen(QColor("#2b6cb0"), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(0, 0, w - 1, h - 1)
        
        painter.setBrush(QColor("#1a365d"))
        painter.setPen(Qt.PenStyle.NoPen)
        c, t, i = 75, 20, 55 
        
        polygons = [
            [(0,0), (c,0), (i,t), (t,t), (t,i), (0,c)], 
            [(w,0), (w-c,0), (w-i,t), (w-t,t), (w-t,i), (w,c)], 
            [(0,h), (c,h), (i,h-t), (t,h-t), (t,h-i), (0,h-c)], 
            [(w,h), (w-c,h), (w-i,h-t), (w-t,h-t), (w-t,h-i), (w,h-c)] 
        ]
        for pts in polygons:
            painter.drawPolygon(QPolygonF([QPointF(px, py) for px, py in pts]))
        
        # --- 4. Crosshairs & Sliders ---
        painter.setPen(QPen(QColor("#63b3ed"), 2))
        for cx, cy in [(w-15, 15), (15, h-15)]: 
            painter.drawLine(cx-4, cy, cx+4, cy)
            painter.drawLine(cx, cy-4, cx, cy+4)
        painter.drawPoint(w-15, h-15) 
        
        painter.setPen(QPen(QColor("#63b3ed"), 3))
        painter.drawLine(w//2 - 120, t, w//2 + 120, t) 
        painter.fillRect(w//2 - 135, t - 2, 10, 7, QColor("#63b3ed"))
        painter.drawLine(w//2 - 180, h-t, w//2 + 180, h-t) 
        painter.fillRect(w//2 - 195, h-t - 2, 10, 7, QColor("#63b3ed"))

class SciFiDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Algorithms Simulation - Main Menu")
        self.resize(1050, 650)
        self.setStyleSheet("QMainWindow { background-color: #0d141f; }")
        
        # Load the settings icon
        icon_path = get_resource_path("settings.ico", "assets/settings.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.last_disk_io = psutil.disk_io_counters()
        self.last_time = time.time()
        
        self.create_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)
        
        # Subprocess tracking
        self.active_process = None
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.check_process_status)
        
        # Add the Cursor Overlay last so it covers absolutely everything
        self.cursor_overlay = CursorOverlay(self)
        self.cursor_overlay.raise_()
        
        # Enable Global Mouse Tracking
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        """Captures global mouse movements and updates the overlay."""
        if event.type() == QEvent.Type.MouseMove and hasattr(self, 'cursor_overlay'):
            # Map the global cursor position directly to the overlay's coordinate space
            pos = self.cursor_overlay.mapFromGlobal(event.globalPosition().toPoint())
            self.cursor_overlay.mouse_pos = pos
            self.cursor_overlay.trail_points.append([pos.x(), pos.y(), 255])
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        """Ensures the cursor overlay always fully covers the window edge-to-edge."""
        super().resizeEvent(event)
        if hasattr(self, 'cursor_overlay'):
            self.cursor_overlay.resize(self.size())

    def create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.container = SciFiFrame()
        c_layout = QVBoxLayout(self.container)
        c_layout.setContentsMargins(45, 45, 45, 35)
        
        header = QHBoxLayout()
        profile = QLabel(f"HOST: {socket.gethostname().upper()}\nDEVICE: {platform.system()} {platform.release()} [{platform.machine()}]".upper())
        profile.setObjectName("ProfileText")
        
        self.btn_devs = QPushButton("SEE DEVELOPERS")
        self.btn_devs.setObjectName("HeaderBtn")
        self.btn_devs.setFixedSize(140, 35)
        self.btn_devs.clicked.connect(self.toggle_view)

        header.addWidget(profile)
        header.addStretch()
        header.addWidget(self.btn_devs)
        
        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.build_dashboard())
        self.stacked.addWidget(self.build_developers())
        
        footer = QHBoxLayout()
        footer.addStretch()
        lbl = QLabel("CREATED BY GROUP 5")
        lbl.setObjectName("SocialLabel")
        footer.addWidget(lbl)

        c_layout.addLayout(header)
        c_layout.addWidget(self.stacked)
        c_layout.addLayout(footer)
        main_layout.addWidget(self.container)
        self.apply_styles()
        
        # Hide standard hardware cursor
        QApplication.setOverrideCursor(Qt.CursorShape.BlankCursor)

    def build_dashboard(self):
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(0, 20, 0, 20)
        
        nav = QVBoxLayout()
        nav.setSpacing(25) 
        nav.addStretch(1) 
        
        modules = [
            ("CPU SCHEDULING", "cpu_scheduling/cpu_scheduling_main.py"), 
            ("MEMORY MANAGEMENT", "memory_management/main.py"), 
            ("VIRTUAL MEMORY", "virtual_memory/main.py"), 
            ("DISK MANAGEMENT", "disk_management/main.py")
        ]
        
        for name, script in modules:
            btn = QPushButton(name)
            btn.setObjectName("MenuBtn")
            btn.setMinimumHeight(65)
            btn.setMaximumWidth(400)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            # Use default argument capture for dynamic buttons
            btn.clicked.connect(lambda chk, n=name, s=script: self.launch(n, s))
            nav.addWidget(btn)
            
        nav.addStretch(1) 
        
        nav_container = QHBoxLayout()
        nav_container.addLayout(nav)
        nav_container.addStretch(1)
        
        scores = QFrame()
        scores.setObjectName("ScoresFrame")
        scores.setMaximumWidth(320)
        s_layout = QVBoxLayout(scores)
        s_layout.setSpacing(10)
        
        title = QLabel("SYSTEM STATUS //////////")
        title.setObjectName("ScoresTitle")
        s_layout.addWidget(title)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        self.stats = {"CPU": QLabel("◈ -- %"), "MEM": QLabel("◎ -- MB"), "DISK": QLabel("❖ -- KB/s")}
        
        for i, (key, label) in enumerate(zip(["CPU LOAD", "MEM USAGE", "DISK I/O"], self.stats.values())):
            label.setObjectName("ScoreValueBox")
            lbl_title = QLabel(key)
            lbl_title.setObjectName("ScoreLabel")
            grid.addWidget(lbl_title, i*2, 0)
            grid.addWidget(label, i*2+1, 0)
            
        s_layout.addLayout(grid)
        s_layout.addStretch()
        
        total = QFrame()
        total.setObjectName("TotalFrame")
        total.setFixedHeight(45) 
        
        t_layout = QHBoxLayout(total)
        t_text = QLabel("Active Processes:")
        t_text.setObjectName("TotalText")
        self.lbl_procs = QLabel("--")
        self.lbl_procs.setObjectName("TotalText")
        self.lbl_procs.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        t_layout.addWidget(t_text)
        t_layout.addWidget(self.lbl_procs)
        s_layout.addWidget(total)
        
        layout.addLayout(nav_container)
        layout.addStretch()
        layout.addWidget(scores)
        return page

    def build_developers(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 20, 0, 20)
        
        title = QLabel("SYSTEM ARCHITECTS & DEVELOPERS")
        title.setObjectName("ScoresTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        devs = QFrame()
        devs.setObjectName("DevsFrame")
        d_layout = QVBoxLayout(devs)
        d_layout.setSpacing(8) 
        
        team = [
            ("AARON CARTAGENA", "Memory Management | Collaborator"),
            ("GELAI BACLEA-AN", "Virtual Memory | Collaborator"),
            ("GERALD TAN ROGADO", "Disk Management | UI/UX Designer\nGitHub: Yozora-apricity"),
            ("JACIN KURT OCAMPO", "CPU Scheduling | Collaborator")
        ]
        
        for i, (name, role) in enumerate(team):
            n_lbl = QLabel(name)
            n_lbl.setObjectName("DevNameText")
            d_layout.addWidget(n_lbl)
            
            r_lbl = QLabel(role)
            r_lbl.setObjectName("DevRoleText")
            d_layout.addWidget(r_lbl)
            
            # Insert Circuit Separator between names
            if i < len(team) - 1:
                d_layout.addWidget(CircuitSeparator())
                
        layout.addWidget(devs)
        layout.addStretch()
        return page

    def toggle_view(self):
        is_dash = self.stacked.currentIndex() == 0
        self.stacked.setCurrentIndex(1 if is_dash else 0)
        self.btn_devs.setText("BACK TO DASHBOARD" if is_dash else "SEE DEVELOPERS")

    def update_stats(self):
        if self.stacked.currentIndex() != 0: return
            
        self.stats["CPU"].setText(f"◈ {psutil.cpu_percent():.1f} %")
        self.stats["MEM"].setText(f"◎ {psutil.virtual_memory().used / (1024**2):,.0f} MB")
        
        cur_io = psutil.disk_io_counters()
        dt = time.time() - self.last_time
        
        if self.last_disk_io and cur_io and dt > 0:
            d_bytes = (cur_io.read_bytes + cur_io.write_bytes) - (self.last_disk_io.read_bytes + self.last_disk_io.write_bytes)
            self.stats["DISK"].setText(f"❖ {(d_bytes / 1024) / dt:,.0f} KB/s")
            
        self.last_disk_io, self.last_time = cur_io, time.time()
        self.lbl_procs.setText(f"{len(psutil.pids()):,}")

    def launch(self, name, script):
        if not script:
            print(f"Path not established for {name}")
            return
            
        # Standardize path across OS 
        script_path = os.path.abspath(script)
        
        if not os.path.exists(script_path):
            print(f"Error: Could not locate file -> {script_path}")
            return
            
        print(f"Launching {name}...")
        self.hide() # Minimizes main menu completely
        
        # Safely launch the sub-module using its own root directory context
        script_dir = os.path.dirname(script_path)
        self.active_process = subprocess.Popen([sys.executable, script_path], cwd=script_dir)
        self.monitor_timer.start(500) 
        
    def check_process_status(self):
        if self.active_process and self.active_process.poll() is not None:
            self.monitor_timer.stop()
            self.active_process = None
            self.show() # Automatically reopen Main Menu

    def apply_styles(self):
        self.setStyleSheet("""
            * { font-family: 'Consolas', 'Courier New', monospace; cursor: none; }
            QLabel#ProfileText { color: #90cdf4; font-weight: bold; font-size: 11px; }
            QPushButton#HeaderBtn { background: #1a365d; border: 1px solid #4299e1; border-radius: 4px; font-weight: bold; font-size: 11px; color: #ebf8ff; z-index: 10; }
            QPushButton#HeaderBtn:hover { background: #2b6cb0; }
            QPushButton#MenuBtn { background: #111b2b; border: 2px solid #2b6cb0; border-radius: 6px; padding: 18px; font-size: 16px; font-weight: bold; color: #63b3ed; min-width: 250px; }
            QPushButton#MenuBtn:hover { background: #2b6cb0; color: #ffffff; }
            QFrame#ScoresFrame, QFrame#DevsFrame { border: 1px solid #2b6cb0; border-radius: 6px; background: rgba(11, 20, 33, 0.85); padding: 15px; }
            QLabel#ScoresTitle { font-size: 16px; font-weight: bold; color: #90cdf4; margin-bottom: 10px; }
            QLabel#ScoreLabel { font-size: 10px; font-weight: bold; color: #a0aec0; margin-top: 5px; }
            QLabel#ScoreValueBox { border: 1px solid #2b6cb0; padding: 6px; font-size: 12px; font-weight: bold; color: #ebf8ff; background: rgba(26, 54, 93, 0.9); }
            QFrame#TotalFrame { background: rgba(43, 108, 176, 0.9); margin-top: 5px; border-radius: 4px; padding: 5px; }
            QLabel#TotalText { color: #ffffff; font-weight: bold; font-size: 13px; }
            QLabel#SocialLabel { font-size: 12px; font-weight: bold; color: #90cdf4; margin-right: 10px; }
            QLabel#DevNameText { font-size: 16px; font-weight: bold; color: #ebf8ff; }
            QLabel#DevRoleText { font-size: 11px; color: #63b3ed; }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SciFiDashboard()
    window.show()
    
    # Safe close event to ensure child processes are terminated if main menu forces close
    app.aboutToQuit.connect(lambda: window.active_process.terminate() if window.active_process else None)
    
    sys.exit(app.exec())