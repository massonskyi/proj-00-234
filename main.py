import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from gui.startmenu import Ui_StartMenu


def main():
    app = QApplication(sys.argv)

    try:
        MainWindow = Ui_StartMenu()
        MainWindow.show()
        sys.exit(app.exec())

    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
