import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PySide6 import QtCore
from PySide6.QtGui import QPainter, QPen, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QTimer, Signal

def qimage_to_cv(image: QImage):
    image = image.convertToFormat(QImage.Format.Format_RGBA8888)
    width = image.width()
    height = image.height()

    ptr = image.bits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
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



class DrawingCanvas(QWidget):
    frame_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)

        self.drawing = False
        self.last_point = QPoint()

        self.frames = [[]]  # list of frames (That has drawing paths or data)
        self.current_frame = 0  # current frame index
        self.redo_stack = []

        # Onion skin settings
        self.show_onion_skin = True
        self.prev_opacity = 80
        self.next_opacity = 60              # Intentopnally Hardcoded for MVP

    def set_frame(self, index):
        self.current_frame = index
        if len(self.frames) <= index:
            self.frames.extend([[] for _ in range(index - len(self.frames) + 1)])
        self.update()

    def get_frame_count(self):
        return len(self.frames)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.redo_stack.clear()  # Clear redo stack on new drawing
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

        # Previous frame onion skin
        if self.show_onion_skin and self.current_frame > 0:
            pen = QPen(QColor(150, 150, 150, self.prev_opacity), 2)
            painter.setPen(pen)
            for path in self.frames[self.current_frame - 1]:
                for i in range(1, len(path)):
                    painter.drawLine(path[i - 1], path[i])

        # Next frame onion skin
        if (
            self.show_onion_skin
            and self.current_frame + 1 < len(self.frames)
            and self.frames[self.current_frame + 1]
        ):
            pen = QPen(QColor(100, 180, 255, self.next_opacity), 2)
            painter.setPen(pen)
            for path in self.frames[self.current_frame + 1]:
                for i in range(1, len(path)):
                    painter.drawLine(path[i - 1], path[i])

        # Current frame
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        for path in self.frames[self.current_frame]:
            for i in range(1, len(path)):
                painter.drawLine(path[i - 1], path[i])

    def undo_last_path(self):
        if self.frames[self.current_frame]:
            # Remove the path and save it to the redo stack
            path = self.frames[self.current_frame].pop()
            self.redo_stack.append(path) 
            self.update()

    def redo_last_path(self):
        if self.redo_stack:
            # Take the last undid item in the stack(Memory) and put it back
            path = self.redo_stack.pop()
            self.frames[self.current_frame].append(path)
            self.update()

    def frame_to_image(self, index):
        image = QImage(self.size(), QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)

        painter = QPainter(image)
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        
        if 0 <= index < len(self.frames):
            for path in self.frames[index]:
                for i in range(1, len(path)):
                    painter.drawLine(path[i - 1], path[i])

        painter.end()
        return image

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TweenCraft")

    

        self.canvas = DrawingCanvas()       # My main drawing canvas(Area)
        self.current_frame = 0            # Current frame index (number)

        # My UI Elements
        self.frame_label = QLabel("Frame 1 / 1")

        self.prev_btn = QPushButton("Prev")
        self.next_btn = QPushButton("Next")
        self.undo_btn = QPushButton("Undo")
        self.redo_btn = QPushButton("Redo")
        self.play_btn = QPushButton("Play")
        self.onion_btn = QPushButton("Toggle Onion Skin")

        self.ai_cleanup_btn = QPushButton("AI Clean-Up")
        self.ai_inbetween_btn = QPushButton("AI In-Between")


        # Frame previews
        self.prev_frame_preview = QLabel()
        self.prev_frame_preview.setFixedSize(100, 75)
        self.prev_frame_preview.setStyleSheet("border: 1px solid gray;")
        self.next_frame_preview = QLabel()
        self.next_frame_preview.setFixedSize(100, 75)
        self.next_frame_preview.setStyleSheet("border: 1px solid gray;")


        # My Connections
        self.prev_btn.clicked.connect(self.prev_frame)
        self.next_btn.clicked.connect(self.next_frame)
        self.undo_btn.clicked.connect(self.canvas.undo_last_path)
        self.redo_btn.clicked.connect(self.canvas.redo_last_path)
        self.play_btn.clicked.connect(self.play_animation)
        self.onion_btn.clicked.connect(self.toggle_onion_skin)

        self.ai_cleanup_btn.clicked.connect(self.ai_cleanup)
        self.ai_inbetween_btn.clicked.connect(self.ai_inbetween)

        # Layout
        top_layout = QHBoxLayout()
        for btn in [
            self.undo_btn,
            self.redo_btn,
            self.prev_btn,
            self.frame_label,
            self.next_btn,
            self.play_btn,
            self.onion_btn,
            self.ai_cleanup_btn,
            self.ai_inbetween_btn,
        ]:
            top_layout.addWidget(btn)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.canvas)

        # Previews Layout
        layout.addWidget(self.canvas)

        # Previews layout
        previews_layout = QHBoxLayout()
        previews_layout.addWidget(self.prev_frame_preview)
        previews_layout.addStretch()
        previews_layout.addWidget(self.next_frame_preview)
        layout.addLayout(previews_layout)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Playback
        self.is_playing = False
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.next_frame)


    
        self.update_frame_label() 
        self.update_frame_previews()


    def update_frame_label(self):
        total_frames = self.canvas.get_frame_count()
        self.frame_label.setText(f"Frame {self.current_frame + 1} / {total_frames}")


    def update_frame_previews(self):
        if self.current_frame > 0:
            prev_img = self.canvas.frame_to_image(self.current_frame - 1)
            prev_img = prev_img.scaled(self.prev_frame_preview.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.prev_frame_preview.setPixmap(prev_img)
        else:
            self.prev_frame_preview.clear()

        if self.current_frame + 1 < self.canvas.get_frame_count():
            next_img = self.canvas.frame_to_image(self.current_frame + 1)
            next_img = next_img.scaled(self.next_frame_preview.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.next_frame_preview.setPixmap(next_img)
        else:
            self.next_frame_preview.clear()



    def last_drawn_frame_index(self):
        for i in range(len(self.canvas.frames) - 1, -1, -1):
            if self.canvas.frames[i]:                           #Tells what the last drawn frame is
                return i
        return 0

    def prev_frame(self):

        if self.current_frame > 0:

            self.current_frame -= 1

            self.canvas.set_frame(self.current_frame)

            self.update_frame_label()
            self.update_frame_previews()

    def next_frame(self):
        if self.is_playing:
            last_frame = self.last_drawn_frame_index()
            if self.current_frame >= last_frame:
                self.current_frame = 0
            else:
                self.current_frame += 1

        else:
                # Manual navigation in editing mode
            if self.current_frame + 1 < self.canvas.get_frame_count():
                self.current_frame += 1
            else:
                self.canvas.frames.append([])  # create new blank frame
                self.current_frame += 1


        self.canvas.set_frame(self.current_frame)
        self.update_frame_label()
        self.update_frame_previews()                        # This allocs me to see the next frame preview

    def play_animation(self):
        if self.play_timer.isActive():
            self.play_timer.stop()
            self.play_btn.setText("Play")
            self.is_playing = False
        else:
            self.is_playing = True
            self.play_timer.start(100)
            self.play_btn.setText("Pause")

    def toggle_onion_skin(self):
        self.canvas.show_onion_skin = not self.canvas.show_onion_skin
        self.canvas.update()

    # AI PLACEHOLDERS, Might as well use OpenCV for this and PyTorch or TensorFlow for ML model integration
    def ai_cleanup(self):
        image = self.canvas.frame_to_image(self.current_frame)
        clean = ai_cleanup_opencv(image)

        clean.save(f"cleanup_frame_{self.current_frame}.png")
        print("AI Clean-Up complete (OpenCV)")


        image.save(f"clean_look frame_{self.current_frame + 1}")
        print("AI image generated successfully")
        # Later: send `image` to ML model

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

        print("AI In-Between frames generated")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
