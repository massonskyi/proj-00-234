from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QPlainTextEdit

from gui.widgets.linenumberarea import LineNumberArea


class CustomTextEdit(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("base")
        self.text_edit.setReadOnly(False)
        self.text_edit.setFont(QFont("Arial", 12))
        self.text_edit.setStyleSheet(
            "QTextEdit { border: none; background-color: #f4f4f4; color: black; }")

        self.line_number_area = LineNumberArea()
        self.line_number_area.setFont(QFont("Courier New", 12))
        self.update_line_numbers()

        self.text_edit.textChanged.connect(self.update_line_numbers)
        self.text_edit.verticalScrollBar().valueChanged.connect(self.sync_scroll)

        layout = QHBoxLayout(self)
        layout.addWidget(self.line_number_area)
        layout.addWidget(self.text_edit)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def update_line_numbers(self):
        line_count = self.text_edit.document().blockCount()
        line_numbers = "\n".join(map(str, range(1, line_count + 1)))
        self.line_number_area.setPlainText(line_numbers)

    def append(self, text):
        self.text_edit.append(text)
        self.update_line_numbers()

    def sync_scroll(self):
        value = self.text_edit.verticalScrollBar().value()
        self.line_number_area.update_scroll(value)

    def set_cursor_position(self, position):
        cursor = self.text_edit.textCursor()
        cursor.setPosition(position)
        self.text_edit.setTextCursor(cursor)
