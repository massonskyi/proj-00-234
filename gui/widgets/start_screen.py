import sys
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap, QMovie
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from config.cfg import EXE_DIR


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Устанавливаем флаг Qt.WindowStaysOnTopHint
        self.setAttribute(Qt.WA_TranslucentBackground)  # Делаем фон окна прозрачным (если нужно)

        self.label = QLabel(self)
        self.movie = QMovie(f"{EXE_DIR}\\assets\\start_screen.gif")
        self.label.setMovie(self.movie)
        self.label.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.label)

        self.setLayout(vbox)

        self.movie.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_movie_playing)
        self.timer.start(50)  # Проверяем каждые 50 мс

    def check_movie_playing(self):
        if self.movie.currentFrameNumber() == self.movie.frameCount() - 1:
            self.movie.stop()
            self.close()
