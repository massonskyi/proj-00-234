import sys
from typing import TextIO

from PySide6.QtGui import (
    QTextCursor,
    QKeyEvent
)
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtCore import Qt
import code


class CustomPyConsole(QPlainTextEdit):
    """
    Class for Custom PyConsole widget.
    """

    def __init__(self, path: str, parent=None) -> None:
        """
        Initialise the Custom PyConsole widget.
        :return: None
        """
        super().__init__(parent)
        self.prompt_style: str | None = None
        self.path: str = path
        self.setWindowTitle('Custom Console')
        self.setReadOnly(False)
        self.history: list = []
        self.number_of_lines: int = 0
        self.historyIndex: int = -1

        self.interpreter: code.InteractiveConsole = code.InteractiveConsole(locals={})
        self.display_system_info()

    def display_system_info(self) -> None:
        """
        Display system information in the console.
        :return: None
        """
        system_info = (
            f"Version: {sys.version}\n"
            f"Name: {sys.thread_info}\n"
        )
        self.number_of_lines += 1
        self.prompt_style = f"{self.path} [{self.number_of_lines}]$ "
        self.number_of_lines += 1
        self.prompt_style = f"{self.path} [{self.number_of_lines}]$ "
        self.insertPlainText(system_info + self.prompt_style)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handle key press event.
        :param event: QKeyEvent
        :return: None
        """
        if event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
            cursor: QTextCursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            line: str = cursor.block().text()[len(self.prompt_style):]
            self.history.append(line)
            self.historyIndex = -1
            self.run_command(line)

        elif event.key() == Qt.Key.Key_Up:
            if self.history:
                self.historyIndex = (self.historyIndex - 1) % len(self.history)
                self.replace_current_line(self.history[self.historyIndex])

        elif event.key() == Qt.Key.Key_Down:
            if self.history:
                self.historyIndex = (self.historyIndex + 1) % len(self.history)
                self.replace_current_line(self.history[self.historyIndex])
        else:
            super().keyPressEvent(event)

    def replace_current_line(self, text: str) -> None:
        """
        Replace the current line with the given text.
        :param text: str
        :return: None
        """
        cursor: QTextCursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(self.prompt_style + text)

    def run_command(self, command: str) -> None:
        """
        Execute the given command on the console. If the command is empty, the console will be cleared.
        :param command: str
        :return: None
        """
        self.insertPlainText('\n')
        old_stdout: TextIO = sys.stdout
        old_stderr: TextIO = sys.stderr
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

    def write(self, text: str) -> None:
        """
        Write the given text to the console.
        :param text: str
        :return: None
        """
        self.insertPlainText(text)

    def writelines(self, lines: list) -> None:
        """
        Write the given list of lines to the console.
        :param lines: list
        :return: None
        """
        for line in lines:
            self.write(line)

    def flush(self) -> None:
        """
        Flush the console.
        :return: None
        """
        pass

    def clear(self) -> None:
        """
        Clear the console.
        :return: None
        """
        self.clear()

