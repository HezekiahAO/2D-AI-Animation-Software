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

        self.prev_btn.clicked.connect(self.prev_frame)
        self.next_btn.clicked.connect(self.next_frame)
        self.undo_btn.clicked.connect(self.canvas.undo_last_path)
        self.save_btn.clicked.connect(self.save_frame)
        self.play_btn.clicked.connect(self.play_animation)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.undo_btn)
        button_layout.addWidget(self.prev_btn)
        button_layout.addWidget(self.frame_label)
        button_layout.addWidget(self.next_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.play_btn)

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
        # If we've reached the last frame or the next frame is empty, loop back to the beginning
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
            print("❌ No frames to play.    Add some drawings first.")
            return
        if self.play_timer.isActive():
            self.play_timer.isActive()
            self.play_timer.stop()
            self.play_btn.setText("Play")
            self.is_playing = False    # This line of code is used to stop the timer when we click the play again to avoid enless loop
        else:
            self.is_playing = True # Once enless loop is avoided, we can now start the drawing on a new frame
            self.play_timer.start(100)  # Frames plays faster at 6.6 fps   10 frames/sec.   Hence 50 frames/sec = 5fps
            self.play_btn.setText("Pause")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
