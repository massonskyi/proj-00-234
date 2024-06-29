import os
import platform

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QTextCursor,
    QKeyEvent
)
from PySide6.QtWidgets import QPlainTextEdit

from gui.Threads.CommandThread import CommandThread


class CustomBashConsole(QPlainTextEdit):
    """
    Custom bash console is a custom QPlainTextEdit that runs a bash command
    """
    def __init__(self, path: str, parent=None) -> None:
        """
        Initialise the custom bash console from QPlainTextEdit.
        """
        super().__init__(parent)
        self.setWindowTitle('Bash Console')
        self.setReadOnly(False)
        self.cwd: str = path
        self.prompt: str = f'{path}$ '
        self.insertPlainText(self.prompt)
        self.commandThread: object = None
        self.display_system_info()

    def display_system_info(self) -> None:
        """
        Display system information in the console.
        :return: None
        """
        system_info = (
            f"System: {platform.system()}\n"
            f"Node Name: {platform.node()}\n"
            f"Release: {platform.release()}\n"
            f"Version: {platform.version()}\n"
            f"Machine: {platform.machine()}\n"
            f"Processor: {platform.processor()}\n"
        )
        self.insertPlainText(system_info + "\n")
        self.insertPlainText(self.prompt)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handle key press events.
        :param event: QKeyEvent
        :return: None
        """
        if event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            line = cursor.block().text()[len(self.prompt):]
            self.run_command(line)
        else:
            super().keyPressEvent(event)

    def run_command(self, command: str) -> None:
        """
        Execute a bash command. If a command is not found, the console will display the command.
        :param command: string command to be executed
        :return: None
        """
        if command.strip().startswith('cd'):
            self.change_directory(command.strip())
        else:
            self.insertPlainText('\n')
            self.setReadOnly(True)
            self.commandThread = CommandThread(command, self.cwd)
            self.commandThread.outputReceived.connect(self.append_output)
            self.commandThread.commandFinished.connect(self.command_finished)
            self.commandThread.start()

    def change_directory(self, command: str) -> None:
        """
        Change the current directory.
        :param command: string command to be executed
        :return: None
        """
        try:
            path: str = command[3:].strip()
            os.chdir(path)
            self.cwd: str = os.getcwd()
            self.prompt: str = f'{self.cwd}$ '
            self.insertPlainText(f'\nChanged directory to {self.cwd}\n')
        except Exception as e:
            self.insertPlainText(f'\nError: {e}\n')
        self.insertPlainText(self.prompt)

    def append_output(self, text: str) -> None:
        """
        Append text to the end of the output.
        :param text: string text to be appended
        :return: None
        """
        self.insertPlainText(text)

    def command_finished(self) -> None:
        """
        Set the console to read only.
        :return: None
        """
        self.insertPlainText(self.prompt)
        self.setReadOnly(False)
