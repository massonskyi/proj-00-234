import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from gui.startmenu import Ui_StartMenu


def main():
    app = QApplication(sys.argv)

    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if not file_path.endswith('.mdth'):
                QMessageBox.critical(None, "Error", "Этот файл невозможно открыть")
                sys.exit(1)

            MainWindow = Ui_StartMenu()
            MainWindow.open_main_window_from_file(file_path)
        else:
            MainWindow = Ui_StartMenu()
            MainWindow.show()

        sys.exit(app.exec())

    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
