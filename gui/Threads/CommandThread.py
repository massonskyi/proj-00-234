import subprocess

from PySide6.QtCore import QThread, Signal


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
