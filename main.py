from PySide6 import QtWidgets

from gui.main_window import Ui_MainWindow

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
