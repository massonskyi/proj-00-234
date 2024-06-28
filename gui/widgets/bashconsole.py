import os
import platform
import sys
import subprocess

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QThread, Signal


class CommandThread(QThread):
    outputReceived = Signal(str)
    commandFinished = Signal()

    def __init__(self, command, cwd=None):
        super().__init__()
        self.command = command
        self.cwd = cwd

    def run(self):
        process = subprocess.Popen(
            self.command,
            shell=True,
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in iter(process.stdout.readline, ''):
            self.outputReceived.emit(line)
        for line in iter(process.stderr.readline, ''):
            self.outputReceived.emit(line)
        process.stdout.close()
        process.stderr.close()
        process.wait()
        self.commandFinished.emit()

class BashConsoleWidget(QPlainTextEdit):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Bash Console')
        self.setReadOnly(False)
        self.cwd = path
        self.prompt = f'{path}$ '
        self.insertPlainText(self.prompt)
        self.commandThread = None
        self.display_system_info()

    def display_system_info(self):
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

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            line = cursor.block().text()[len(self.prompt):]
            self.run_command(line)
        else:
            super().keyPressEvent(event)

    def run_command(self, command):
        if command.strip().startswith('cd'):
            self.change_directory(command.strip())
        else:
            self.insertPlainText('\n')
            self.setReadOnly(True)
            self.commandThread = CommandThread(command, self.cwd)
            self.commandThread.outputReceived.connect(self.append_output)
            self.commandThread.commandFinished.connect(self.command_finished)
            self.commandThread.start()

    def change_directory(self, command):
        try:
            path = command[3:].strip()
            os.chdir(path)
            self.cwd = os.getcwd()
            self.prompt = f'{self.cwd}$ '
            self.insertPlainText(f'\nChanged directory to {self.cwd}\n')
        except Exception as e:
            self.insertPlainText(f'\nError: {e}\n')
        self.insertPlainText(self.prompt)

    def append_output(self, text):
        self.insertPlainText(text)

    def command_finished(self):
        self.insertPlainText(self.prompt)
        self.setReadOnly(False)

