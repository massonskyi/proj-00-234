import sys
import subprocess

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QThread, Signal


class CommandThread(QThread):
    outputReceived = Signal(str)
    commandFinished = Signal()

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in iter(process.stdout.readline, ''):
            self.outputReceived.emit(line)
        for line in iter(process.stderr.readline, ''):
            self.outputReceived.emit(line)
        process.stdout.close()
        process.stderr.close()
        process.wait()
        self.commandFinished.emit()


class BashConsoleWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Bash Console')
        self.setReadOnly(False)
        self.prompt = '$ '
        self.insertPlainText(self.prompt)
        self.commandThread = None

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            line = cursor.block().text()[len(self.prompt):]
            self.run_command(line)
        else:
            super().keyPressEvent(event)

    def run_command(self, command):
        self.insertPlainText('\n')
        self.setReadOnly(True)
        self.commandThread = CommandThread(command)
        self.commandThread.outputReceived.connect(self.append_output)
        self.commandThread.commandFinished.connect(self.command_finished)
        self.commandThread.start()

    def append_output(self, text):
        self.insertPlainText(text)

    def command_finished(self):
        self.insertPlainText(self.prompt)
        self.setReadOnly(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    console = BashConsoleWidget()
    layout.addWidget(console)
    window.setLayout(layout)
    window.setWindowTitle('PySide6 Bash Console Widget')
    window.show()
    sys.exit(app.exec())
