import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QApplication, QMenuBar, QMenu, QStatusBar, QTextEdit, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Custom Status Bar Example')

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Initialize status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.current_state = "Ready"
        self.file_encoding = "UTF-8"
        self.current_file_path = ""
        self.read_only = False

        self.create_actions()
        self.create_menus()

        self.update_status_bar()

    def create_actions(self):
        self.open_action = QAction("Open...", self)
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("Save As...", self)
        self.save_action.triggered.connect(self.save_file)

        self.read_only_action = QAction("Toggle Read-Only", self)
        self.read_only_action.triggered.connect(self.toggle_read_only)

    def create_menus(self):
        menu_bar = QMenuBar()

        file_menu = QMenu("File", self)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.read_only_action)

        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_path:
            self.current_file_path = file_path
            with open(file_path, 'r', encoding=self.file_encoding) as file:
                self.text_edit.setPlainText(file.read())
            self.current_state = "File Opened"
            self.update_status_bar()

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As")
        if file_path:
            self.current_file_path = file_path
            with open(file_path, 'w', encoding=self.file_encoding) as file:
                file.write(self.text_edit.toPlainText())
            self.current_state = "File Saved"
            self.update_status_bar()

    def toggle_read_only(self):
        self.read_only = not self.read_only
        self.text_edit.setReadOnly(self.read_only)
        self.current_state = "Read-Only" if self.read_only else "Editable"
        self.update_status_bar()

    def update_status_bar(self):
        status = f"State: {self.current_state} | Encoding: {self.file_encoding} | Path: {self.current_file_path} | {'Read-Only' if self.read_only else 'Editable'}"
        self.status_bar.showMessage(status)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()