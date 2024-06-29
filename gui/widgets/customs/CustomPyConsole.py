import os
import sys

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal
import code
import threading


class CustomPyConsole(QPlainTextEdit):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self.setWindowTitle('Custom Console')
        self.setReadOnly(False)
        self.history = []
        self.number_of_lines = 0
        self.historyIndex = -1

        self.interpreter = code.InteractiveConsole(locals={})
        self.display_system_info()

    def display_system_info(self):
        system_info = (
            f"Version: {sys.version}\n"
            f"Name: {sys.thread_info}\n"
        )
        self.number_of_lines += 1
        self.prompt_style = f"{self.path} [{self.number_of_lines}]$ "
        self.number_of_lines += 1
        self.prompt_style = f"{self.path} [{self.number_of_lines}]$ "
        self.insertPlainText(system_info + self.prompt_style)


    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            line = cursor.block().text()[len(self.prompt_style):]
            self.history.append(line)
            self.historyIndex = -1
            self.run_command(line)
        elif event.key() == Qt.Key_Up:
            if self.history:
                self.historyIndex = (self.historyIndex - 1) % len(self.history)
                self.replace_current_line(self.history[self.historyIndex])
        elif event.key() == Qt.Key_Down:
            if self.history:
                self.historyIndex = (self.historyIndex + 1) % len(self.history)
                self.replace_current_line(self.history[self.historyIndex])
        else:
            super().keyPressEvent(event)

    def replace_current_line(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(self.prompt_style + text)

    def run_command(self, command):
        self.insertPlainText('\n')
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self
        try:
            self.interpreter.push(command)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        self.number_of_lines += 1
        self.prompt_style = f"{self.path} [{self.number_of_lines}]$ "
        self.insertPlainText(self.prompt_style)

    def write(self, text):
        self.insertPlainText(text)

    def flush(self):
        pass

