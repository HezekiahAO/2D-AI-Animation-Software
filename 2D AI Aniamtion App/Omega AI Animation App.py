import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PySide6.QtGui import QPainter, QPen, QMouseEvent, QImage
from PySide6.QtCore import Qt, QPoint, QTimer


class DrawingCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)
        self.drawing = False
        self.last_point = QPoint()

        self.frames = [[]]  # Store frame drawings
        self.current_frame = 0

    def set_frame(self, index):
        self.current_frame = index
        if len(self.frames) <= index:
            self.frames.extend([[] for _ in range(index - len(self.frames) + 1)])
        self.update()

    def get_frame_count(self):
        return len(self.frames)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
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
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)

        for path in self.frames[self.current_frame]:
            for i in range(1, len(path)):
                painter.drawLine(path[i - 1], path[i])

    def undo_last_path(self):
        if self.frames[self.current_frame]:
            self.frames[self.current_frame].pop()
            self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Omega 2D Animator – MVP Level 2")

        self.canvas = DrawingCanvas()
        self.current_frame = 0

        self.frame_label = QLabel("Frame 1 / 1")
        self.prev_btn = QPushButton("Prev Frame")
        self.next_btn = QPushButton("Next Frame")
        self.undo_btn = QPushButton("Undo")
        self.save_btn = QPushButton("Save Frame")
        self.play_btn = QPushButton("Play")
        self.export_btn = QPushButton("Export as GIF")

        self.prev_btn.clicked.connect(self.prev_frame)
        self.next_btn.clicked.connect(self.next_frame)
        self.undo_btn.clicked.connect(self.canvas.undo_last_path)
        self.save_btn.clicked.connect(self.save_frame)
        self.play_btn.clicked.connect(self.play_animation)
        self.export_btn.clicked.connect(self.export_gif)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.undo_btn)
        button_layout.addWidget(self.prev_btn)
        button_layout.addWidget(self.frame_label)
        button_layout.addWidget(self.next_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.play_btn)
        button_layout.addWidget(self.export_btn)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.update_frame_label()
        self.is_playing = False

        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.next_frame)

    def update_frame_label(self):
        total = self.canvas.get_frame_count()
        self.frame_label.setText(f"Frame {self.current_frame + 1} / {total}")

    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.canvas.set_frame(self.current_frame)
            self.update_frame_label()

    def next_frame(self):
        next_index = self.current_frame + 1

        if self.is_playing:
            if next_index >= self.canvas.get_frame_count() or not self.canvas.frames[next_index]:
                self.current_frame = 0
                self.canvas.set_frame(self.current_frame)
                self.update_frame_label()
                return

        self.current_frame = next_index
        self.canvas.set_frame(self.current_frame)
        self.update_frame_label()

    def save_frame(self):
        if not (0 <= self.current_frame < self.canvas.get_frame_count()):
            print("❌ Invalid frame index. Cannot save.")
            return

        image = QImage(self.canvas.size(), QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)

        painter = QPainter(image)
        self.canvas.render(image)
        painter.end()

        filename = f"frame_{self.current_frame + 1}.png"
        image.save(filename)
        print(f"✅ Saved: {filename}")

    def play_animation(self):
        if not self.canvas.get_frame_count():
            print("❌ No frames to play. Add some drawings first.")
            return
        if self.play_timer.isActive():
            self.play_timer.stop()
            self.play_btn.setText("Play")
            self.is_playing = False
        else:
            self.is_playing = True
            self.play_timer.start(100)  # 10 fps = 100ms per frame
            self.play_btn.setText("Pause")

    def export_gif(self):
        from PIL import Image

        frames = []
        canvas_size = self.canvas.size()
        width, height = canvas_size.width(), canvas_size.height()

        for i, paths in enumerate(self.canvas.frames):
            if not paths:
                continue

            image = QImage(self.canvas.size(), QImage.Format.Format_ARGB32)
            image.fill(Qt.GlobalColor.white)

            painter = QPainter(image)
            self.canvas.render(image)
            self.canvas.set_frame(i)
            painter.end()


            ptr = image.bits()
            ptr = ptr[:image.sizeInBytes()]
            pil_img = Image.frombytes("RGBA", (width, height), bytes(ptr))

            pil_img = Image.frombytes("RGBA", (width, height), ptr)
            frames.append(pil_img.convert("P"))

        if not frames:
            print("❌ No valid frames to export.")
            return

        frames[0].save(
            "animation.gif",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0
        )
        print("✅ Exported animation.gif successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
