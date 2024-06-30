import sys
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap, QMovie
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QSplashScreen

from config.cfg import EXE_DIR


class SplashScreen(QLabel):
    _finished = Signal()

    def __init__(self, movie_file):
        super().__init__()
        self.movie = QMovie(movie_file)
        self.setMovie(self.movie)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.movie.frameChanged.connect(self.check_if_finished)
        self.resize(650, 500)
        self.center()
        self.setScaledContents(True)

    def start(self):
        self.movie.start()

    def check_if_finished(self):
        if self.movie.currentFrameNumber() == self.movie.frameCount() - 1:
            self.movie.stop()
            self.close()
            self._finished.emit()

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
