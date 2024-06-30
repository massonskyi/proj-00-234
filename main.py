import sys
import time

from PySide6.QtCore import QThread, QTimer
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from config.cfg import EXE_DIR
from gui.startmenu import Ui_StartMenu
from gui.widgets.start_screen import SplashScreen


def main():
    app = QApplication(sys.argv)
    splash_screen = SplashScreen(f"{EXE_DIR}\\assets\\start_screen.gif")
    splash_screen.show()
    splash_screen.start()

    main_window = Ui_StartMenu()

    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if not file_path.endswith('.mdth'):
                QMessageBox.critical(None, "Error", "Этот файл невозможно открыть")
                sys.exit(1)
            splash_screen._finished.connect(lambda: main_window.open_main_window_from_file(file_path))
        else:
            splash_screen._finished.connect(main_window.show)

        sys.exit(app.exec())

    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()