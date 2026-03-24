import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QSizePolicy, QScrollArea, QToolButton
)
from PySide6 import QtCore
from PySide6.QtGui import (
    QPainter, QPen, QMouseEvent, QImage, QColor, QIcon,
    QPixmap, QPainterPath, QFont, QFontDatabase
)
from PySide6.QtCore import Qt, QPoint, QTimer, Signal, QSize, QRect


# ─────────────────────────────────────────────────────────
#  OpenCV helpers (unchanged logic)
# ─────────────────────────────────────────────────────────

def qimage_to_cv(image: QImage):
    image = image.convertToFormat(QImage.Format.Format_RGBA8888)
    width, height = image.width(), image.height()
    p = image.bits()
    arr = np.frombuffer(p, np.uint8, count=height * width * 4).reshape((height, width, 4))
    return cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)


def cv_to_qimage(gray):
    h, w = gray.shape
    return QImage(gray.data, w, h, w, QImage.Format.Format_Grayscale8)


def ai_cleanup_opencv(image: QImage) -> QImage:
    gray = qimage_to_cv(image)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    inverted = cv2.bitwise_not(edges)
    return cv_to_qimage(inverted)


def ai_generate_inbetweens(frame_a: QImage, frame_b: QImage, count=2):
    a = qimage_to_cv(frame_a)
    b = qimage_to_cv(frame_b)
    results = []
    for i in range(1, count + 1):
        alpha = i / (count + 1)
        blended = cv2.addWeighted(a, 1 - alpha, b, alpha, 0)
        results.append(cv_to_qimage(blended))
    return results


# ─────────────────────────────────────────────────────────
#  Palette & style constants
# ─────────────────────────────────────────────────────────

DARK_BG        = "#1a1a1e"
PANEL_BG       = "#242428"
TOOLBAR_BG     = "#2a2a2f"
SURFACE        = "#303036"
SURFACE_HOVER  = "#3a3a42"
BORDER         = "#3f3f48"
ACCENT         = "#e05252"          # red accent (matches reference)
ACCENT_DIM     = "#993838"
TEXT_PRIMARY   = "#e8e8ec"
TEXT_SECONDARY = "#8a8a96"
CANVAS_BG      = "#f5f5f0"          # off-white canvas (like paper)

ICON_BTN_STYLE = f"""
    QToolButton {{
        background: transparent;
        border: none;
        border-radius: 6px;
        color: {TEXT_SECONDARY};
        font-size: 18px;
        padding: 6px;
    }}
    QToolButton:hover {{
        background: {SURFACE_HOVER};
        color: {TEXT_PRIMARY};
    }}
    QToolButton:checked {{
        background: {ACCENT};
        color: white;
    }}
"""

FLAT_BTN_STYLE = f"""
    QPushButton {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 6px;
        color: {TEXT_PRIMARY};
        font-size: 12px;
        font-weight: 600;
        padding: 6px 10px;
    }}
    QPushButton:hover {{
        background: {SURFACE_HOVER};
        border-color: #5a5a68;
    }}
    QPushButton:pressed {{
        background: {ACCENT_DIM};
        border-color: {ACCENT};
    }}
"""

ACCENT_BTN_STYLE = f"""
    QPushButton {{
        background: {ACCENT};
        border: none;
        border-radius: 6px;
        color: white;
        font-size: 13px;
        font-weight: 700;
        padding: 8px 14px;
    }}
    QPushButton:hover {{
        background: #e86060;
    }}
    QPushButton:pressed {{
        background: {ACCENT_DIM};
    }}
"""

TIMELINE_CELL_STYLE = f"""
    QLabel {{
        background: {SURFACE};
        border: 1.5px solid {BORDER};
        border-radius: 4px;
        color: {TEXT_SECONDARY};
        font-size: 10px;
    }}
"""

TIMELINE_CELL_ACTIVE = f"""
    QLabel {{
        background: {ACCENT};
        border: 1.5px solid #ff7070;
        border-radius: 4px;
        color: white;
        font-size: 10px;
    }}
"""


# ─────────────────────────────────────────────────────────
#  Icon helpers (text-based glyphs — no external assets)
# ─────────────────────────────────────────────────────────

def icon_btn(glyph: str, tooltip: str, checkable=False) -> QToolButton:
    btn = QToolButton()
    btn.setText(glyph)
    btn.setToolTip(tooltip)
    btn.setCheckable(checkable)
    btn.setFixedSize(40, 40)
    btn.setStyleSheet(ICON_BTN_STYLE)
    return btn


def flat_btn(text: str, tooltip: str = "") -> QPushButton:
    btn = QPushButton(text)
    btn.setToolTip(tooltip)
    btn.setStyleSheet(FLAT_BTN_STYLE)
    return btn


def accent_btn(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setStyleSheet(ACCENT_BTN_STYLE)
    return btn


# ─────────────────────────────────────────────────────────
#  Drawing canvas (same logic, new look)
# ─────────────────────────────────────────────────────────

class DrawingCanvas(QWidget):
    frame_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(700, 520)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.CrossCursor)

        self.drawing = False
        self.last_point = QPoint()

        self.frames = [[]]
        self.current_frame = 0
        self.redo_stack = []

        self.show_onion_skin = True
        self.prev_opacity = 80
        self.next_opacity = 60

    def set_frame(self, index):
        self.current_frame = index
        while len(self.frames) <= index:
            self.frames.append([])
        self.update()

    def get_frame_count(self):
        return len(self.frames)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.redo_stack.clear()
            self.drawing = True
            self.last_point = event.position().toPoint()
            self.frames[self.current_frame].append([self.last_point])

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing:
            point = event.position().toPoint()
            self.frames[self.current_frame][-1].append(point)
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Canvas background (paper-like)
        painter.fillRect(self.rect(), QColor(CANVAS_BG))

        # Subtle grid
        painter.setPen(QPen(QColor("#e0e0d8"), 0.5, Qt.PenStyle.SolidLine))
        step = 40
        for x in range(0, self.width(), step):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), step):
            painter.drawLine(0, y, self.width(), y)

        # Previous frame onion skin (warm tint)
        if self.show_onion_skin and self.current_frame > 0:
            pen = QPen(QColor(220, 120, 80, self.prev_opacity), 2)
            painter.setPen(pen)
            for path in self.frames[self.current_frame - 1]:
                for i in range(1, len(path)):
                    painter.drawLine(path[i - 1], path[i])

        # Next frame onion skin (cool tint)
        if (
            self.show_onion_skin
            and self.current_frame + 1 < len(self.frames)
            and self.frames[self.current_frame + 1]
        ):
            pen = QPen(QColor(80, 160, 220, self.next_opacity), 2)
            painter.setPen(pen)
            for path in self.frames[self.current_frame + 1]:
                for i in range(1, len(path)):
                    painter.drawLine(path[i - 1], path[i])

        # Current frame (black ink)
        pen = QPen(QColor("#1a1a1a"), 2.5)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        for path in self.frames[self.current_frame]:
            for i in range(1, len(path)):
                painter.drawLine(path[i - 1], path[i])

    def undo_last_path(self):
        if self.frames[self.current_frame]:
            path = self.frames[self.current_frame].pop()
            self.redo_stack.append(path)
            self.update()

    def redo_last_path(self):
        if self.redo_stack:
            path = self.redo_stack.pop()
            self.frames[self.current_frame].append(path)
            self.update()

    def frame_to_image(self, index):
        image = QImage(self.size(), QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(Qt.GlobalColor.black, 2.5)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        if 0 <= index < len(self.frames):
            for path in self.frames[index]:
                for i in range(1, len(path)):
                    painter.drawLine(path[i - 1], path[i])
        painter.end()
        return image


# ─────────────────────────────────────────────────────────
#  Timeline thumbnail cell
# ─────────────────────────────────────────────────────────

class FrameCell(QWidget):
    clicked = Signal(int)

    def __init__(self, index: int, parent=None):
        super().__init__(parent)
        self.index = index
        self.is_active = False
        self.thumb: QPixmap | None = None
        self.setFixedSize(72, 56)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_active(self, active: bool):
        self.is_active = active
        self.update()

    def set_thumb(self, img: QImage):
        self.thumb = QPixmap.fromImage(img.scaled(
            68, 48,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.update()

    def mousePressEvent(self, _event):
        self.clicked.emit(self.index)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Border & background
        border_color = QColor(ACCENT) if self.is_active else QColor(BORDER)
        bg_color     = QColor("#3a1a1a") if self.is_active else QColor(SURFACE)
        p.setBrush(bg_color)
        p.setPen(QPen(border_color, 1.5))
        p.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 5, 5)

        # Thumbnail or empty placeholder
        if self.thumb:
            # Draw thumbnail centered
            tx = (self.width() - self.thumb.width()) // 2
            ty = (self.height() - self.thumb.height()) // 2 - 4
            p.drawPixmap(tx, ty, self.thumb)
        else:
            p.setPen(QColor(TEXT_SECONDARY))
            p.setFont(QFont("Arial", 16))
            p.drawText(QRect(0, 0, self.width(), self.height() - 8),
                       Qt.AlignmentFlag.AlignCenter, "+")

        # Frame number badge
        badge_color = QColor(ACCENT) if self.is_active else QColor(TOOLBAR_BG)
        p.setBrush(badge_color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(4, self.height() - 16, 22, 12, 3, 3)
        p.setPen(QColor("white") if self.is_active else QColor(TEXT_SECONDARY))
        p.setFont(QFont("Arial", 8, QFont.Weight.Bold))
        p.drawText(QRect(4, self.height() - 16, 22, 12),
                   Qt.AlignmentFlag.AlignCenter, str(self.index + 1))


# ─────────────────────────────────────────────────────────
#  Separator helper
# ─────────────────────────────────────────────────────────

def h_sep():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet(f"color: {BORDER}; background: {BORDER}; max-height: 1px;")
    return line


def v_sep():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.VLine)
    line.setStyleSheet(f"color: {BORDER}; background: {BORDER}; max-width: 1px;")
    return line


# ─────────────────────────────────────────────────────────
#  Main window
# ─────────────────────────────────────────────────────────

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TweenCraft")
        self.setMinimumSize(1100, 720)
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background: {PANEL_BG}; color: {TEXT_PRIMARY}; }}
            QScrollArea {{ background: {DARK_BG}; border: none; }}
            QScrollBar:horizontal {{
                background: {PANEL_BG}; height: 6px; border: none;
            }}
            QScrollBar::handle:horizontal {{
                background: {BORDER}; border-radius: 3px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QToolTip {{
                background: {SURFACE}; color: {TEXT_PRIMARY};
                border: 1px solid {BORDER}; padding: 4px 8px;
                border-radius: 4px;
            }}
        """)

        self.canvas = DrawingCanvas()
        self.current_frame = 0
        self.is_playing = False
        self.frame_cells: list[FrameCell] = []

        self._build_ui()

        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.next_frame)

        self.update_timeline()

    # ── UI construction ────────────────────────────────────

    def _build_ui(self):
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        self.setCentralWidget(root)

        # ── Top bar ──────────────────────────────────────
        top_bar = self._build_top_bar()
        root_layout.addWidget(top_bar)
        root_layout.addWidget(h_sep())

        # ── Middle: left sidebar + canvas + right sidebar ──
        middle = QHBoxLayout()
        middle.setContentsMargins(0, 0, 0, 0)
        middle.setSpacing(0)

        left_panel = self._build_left_panel()
        right_panel = self._build_right_panel()

        middle.addWidget(left_panel)
        middle.addWidget(v_sep())
        middle.addWidget(self.canvas, stretch=1)
        middle.addWidget(v_sep())
        middle.addWidget(right_panel)

        middle_widget = QWidget()
        middle_widget.setLayout(middle)
        root_layout.addWidget(middle_widget, stretch=1)

        root_layout.addWidget(h_sep())

        # ── Bottom: timeline ─────────────────────────────
        bottom = self._build_timeline()
        root_layout.addWidget(bottom)

    def _build_top_bar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(44)
        bar.setStyleSheet(f"background: {TOOLBAR_BG};")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        # App name
        title = QLabel("TweenCraft")
        title.setStyleSheet(f"""
            color: {TEXT_PRIMARY};
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 1px;
        """)
        layout.addWidget(title)

        # Accent dot
        dot = QLabel("●")
        dot.setStyleSheet(f"color: {ACCENT}; font-size: 8px;")
        layout.addWidget(dot)
        layout.addSpacing(12)

        # Undo / Redo
        self.undo_btn = icon_btn("↩", "Undo  (Ctrl+Z)")
        self.redo_btn = icon_btn("↪", "Redo  (Ctrl+Y)")
        self.undo_btn.clicked.connect(self.canvas.undo_last_path)
        self.redo_btn.clicked.connect(self.canvas.redo_last_path)
        layout.addWidget(self.undo_btn)
        layout.addWidget(self.redo_btn)
        layout.addWidget(v_sep())
        layout.addSpacing(4)

        # Frame counter
        self.frame_label = QLabel("Frame  1 / 1")
        self.frame_label.setStyleSheet(f"""
            color: {TEXT_SECONDARY};
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
        """)
        layout.addWidget(self.frame_label)

        layout.addStretch()

        # AI buttons
        self.ai_cleanup_btn = flat_btn("✦ AI Clean-Up", "Clean up current frame lines")
        self.ai_inbetween_btn = flat_btn("✦ AI In-Between", "Generate in-between frames")
        self.ai_cleanup_btn.clicked.connect(self.ai_cleanup)
        self.ai_inbetween_btn.clicked.connect(self.ai_inbetween)
        layout.addWidget(self.ai_cleanup_btn)
        layout.addWidget(self.ai_inbetween_btn)

        return bar

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(52)
        panel.setStyleSheet(f"background: {TOOLBAR_BG};")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(6, 10, 6, 10)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Tool buttons (drawing tools — visual only for now, eraser/shape etc.)
        tools = [
            ("✏", "Pencil (active)", True),
            ("◯", "Ellipse tool", False),
            ("⬜", "Rectangle tool", False),
            ("⬡", "Polygon tool", False),
            ("↖", "Selection", False),
        ]
        self.tool_group: list[QToolButton] = []
        for glyph, tip, checked in tools:
            btn = icon_btn(glyph, tip, checkable=True)
            btn.setChecked(checked)
            btn.clicked.connect(self._make_tool_selector(btn))
            self.tool_group.append(btn)
            layout.addWidget(btn)

        layout.addSpacing(8)
        layout.addWidget(h_sep())
        layout.addSpacing(8)

        # Extra tools
        for glyph, tip in [("🪣", "Fill"), ("𝑻", "Text"), ("♪", "Sound marker")]:
            layout.addWidget(icon_btn(glyph, tip))

        layout.addStretch()
        return panel

    def _make_tool_selector(self, target_btn: QToolButton):
        def _select():
            for btn in self.tool_group:
                btn.setChecked(btn is target_btn)
        return _select

    def _build_right_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(52)
        panel.setStyleSheet(f"background: {TOOLBAR_BG};")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(6, 10, 6, 10)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Delete frame
        del_btn = icon_btn("🗑", "Delete frame")
        del_btn.clicked.connect(self._delete_frame)
        layout.addWidget(del_btn)

        layout.addSpacing(4)

        # Onion skin toggle
        self.onion_btn = icon_btn("⚗", "Toggle Onion Skin", checkable=True)
        self.onion_btn.setChecked(True)
        self.onion_btn.clicked.connect(self.toggle_onion_skin)
        layout.addWidget(self.onion_btn)

        layout.addWidget(h_sep())

        # Play / Pause
        self.play_btn = icon_btn("▶", "Play / Pause")
        self.play_btn.setCheckable(True)
        self.play_btn.clicked.connect(self.play_animation)
        layout.addWidget(self.play_btn)

        # Prev / Next
        self.prev_btn = icon_btn("⏮", "Previous frame")
        self.next_btn = icon_btn("⏭", "Next frame")
        self.prev_btn.clicked.connect(self.prev_frame)
        self.next_btn.clicked.connect(self.next_frame)
        layout.addWidget(self.prev_btn)
        layout.addWidget(self.next_btn)

        layout.addStretch()

        # Add-frame button at bottom
        add_btn = icon_btn("+", "Add new frame")
        add_btn.setStyleSheet(ICON_BTN_STYLE + f"""
            QToolButton {{ color: {ACCENT}; font-size: 22px; font-weight: bold; }}
        """)
        add_btn.clicked.connect(self._add_frame)
        layout.addWidget(add_btn)

        return panel

    def _build_timeline(self) -> QWidget:
        container = QWidget()
        container.setFixedHeight(88)
        container.setStyleSheet(f"background: {PANEL_BG};")

        outer = QHBoxLayout(container)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(8)

        # Left label
        label = QLabel("TIMELINE")
        label.setFixedWidth(66)
        label.setStyleSheet(f"""
            color: {TEXT_SECONDARY};
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 2px;
            padding-top: 20px;
        """)
        outer.addWidget(label)
        outer.addWidget(v_sep())

        # Scrollable cell area
        self.timeline_scroll = QScrollArea()
        self.timeline_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.timeline_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.timeline_scroll.setWidgetResizable(False)
        self.timeline_scroll.setStyleSheet(f"background: {PANEL_BG}; border: none;")
        self.timeline_scroll.setFixedHeight(76)

        self.timeline_inner = QWidget()
        self.timeline_inner.setStyleSheet(f"background: {PANEL_BG};")
        self.timeline_layout = QHBoxLayout(self.timeline_inner)
        self.timeline_layout.setContentsMargins(4, 4, 4, 4)
        self.timeline_layout.setSpacing(6)
        self.timeline_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.timeline_scroll.setWidget(self.timeline_inner)
        outer.addWidget(self.timeline_scroll, stretch=1)

        return container

    # ── Frame navigation helpers ───────────────────────────

    def update_frame_label(self):
        total = self.canvas.get_frame_count()
        self.frame_label.setText(f"Frame  {self.current_frame + 1} / {total}")

    def update_timeline(self):
        # Rebuild cells
        while self.timeline_layout.count():
            item = self.timeline_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        self.frame_cells.clear()

        for i in range(self.canvas.get_frame_count()):
            cell = FrameCell(i)
            cell.set_active(i == self.current_frame)
            # Set thumbnail if frame has content
            if self.canvas.frames[i]:
                img = self.canvas.frame_to_image(i)
                cell.set_thumb(img)
            cell.clicked.connect(self._jump_to_frame)
            self.timeline_layout.addWidget(cell)
            self.frame_cells.append(cell)
            self.frame_cells.append(cell)

        self.timeline_inner.adjustSize()
        self.timeline_inner.updateGeometry()
        self.timeline_scroll.setMinimumHeight(0)
        self.timeline_scroll.update()

        if self.frame_cells:   
            active_cell = self.frame_cells[self.current_frame]
            self.timeline_scroll.ensureWidgetVisible(active_cell)


    def _jump_to_frame(self, index: int):
        self.current_frame = index
        self.canvas.set_frame(self.current_frame)
        self.update_frame_label()
        self.update_timeline()

    def last_drawn_frame_index(self):
        for i in range(len(self.canvas.frames) - 1, -1, -1):
            if self.canvas.frames[i]:
                return i
        return 0

    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.canvas.set_frame(self.current_frame)
            self.update_frame_label()
            self.update_timeline()

    def next_frame(self):
        if self.is_playing:
            last_frame = self.last_drawn_frame_index()
            self.current_frame = 0 if self.current_frame >= last_frame else self.current_frame + 1
        else:
            if self.current_frame + 1 < self.canvas.get_frame_count():
                self.current_frame += 1
            else:
                self.canvas.frames.append([])
                self.current_frame += 1

        self.canvas.set_frame(self.current_frame)
        self.update_frame_label()
        self.update_timeline()

    def _add_frame(self):
        self.canvas.frames.append([])
        self.current_frame = len(self.canvas.frames) - 1
        self.canvas.set_frame(self.current_frame)
        self.update_frame_label()
        self.update_timeline()

    def _delete_frame(self):
        if len(self.canvas.frames) <= 1:
            return
        self.canvas.frames.pop(self.current_frame)
        self.current_frame = min(self.current_frame, len(self.canvas.frames) - 1)
        self.canvas.set_frame(self.current_frame)
        self.update_frame_label()
        self.update_timeline()

    def play_animation(self):
        if self.play_timer.isActive():
            self.play_timer.stop()
            self.play_btn.setText("▶")
            self.play_btn.setChecked(False)
            self.is_playing = False
        else:
            self.is_playing = True
            self.play_timer.start(100)
            self.play_btn.setText("⏸")
            self.play_btn.setChecked(True)

    def toggle_onion_skin(self):
        self.canvas.show_onion_skin = not self.canvas.show_onion_skin
        self.onion_btn.setChecked(self.canvas.show_onion_skin)
        self.canvas.update()

    # ── AI actions (unchanged logic) ───────────────────────

    def ai_cleanup(self):
        image = self.canvas.frame_to_image(self.current_frame)
        clean = ai_cleanup_opencv(image)
        clean.save(f"cleanup_frame_{self.current_frame}.png")
        print("AI Clean-Up complete (OpenCV)")

    def ai_inbetween(self):
        if self.current_frame + 1 >= self.canvas.get_frame_count():
            print("No next frame available")
            return

        frame_a = self.canvas.frame_to_image(self.current_frame)
        frame_b = self.canvas.frame_to_image(self.current_frame + 1)
        inbetweens = ai_generate_inbetweens(frame_a, frame_b, count=2)

        insert_index = self.current_frame + 1
        for img in inbetweens:
            self.canvas.frames.insert(insert_index, [])
            img.save(f"inbetween_{insert_index}.png")
            insert_index += 1

        self.update_frame_label()
        self.update_timeline()
        print("AI In-Between frames generated")


# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())