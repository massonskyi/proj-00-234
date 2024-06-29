from PySide6.QtCore import QThread


class CallbackThread(QThread):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def run(self):
        self.target()
