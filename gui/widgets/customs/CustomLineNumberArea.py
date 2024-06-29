from PySide6.QtGui import QFont, QTextCursor, Qt
from PySide6.QtWidgets import QPlainTextEdit, QSizePolicy


class CustomLineNumberArea(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #e0e0e0; color: #555555;padding-left: 5px;")
        self.setFont(QFont("Courier New", 12))
        self.setFixedWidth(65)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def update_scroll(self, value):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(value)
