import os
import shutil

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox

from gui.startmenu import Ui_StartMenu


def check_configuration():
    import os
    if not os.path.exists("./configuration_config_mdt.json"):
        QMessageBox.information(None, "Warning",
                                "Configuration file not found. Run the configuration_config_mdt.py script.")
        from utils.configuration_config_mdt import ConfigurationMDTH
        try:
            ConfigurationMDTH.create_configuration_config_mdt().save_as_json()
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False
        else:
            QMessageBox.information(None, "Success", "Configuration file created successfully.")
            return True

def remove_pycache_dirs(start_path='.'):
    """
    Recursively remove all __pycache__ directories starting from the given directory.
    :param start_path: The root directory from which to start the search
    """
    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                shutil.rmtree(pycache_path)
                print(f"Removed: {pycache_path}")

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    check_configuration()
    remove_pycache_dirs()
    try:
        MainWindow = Ui_StartMenu()
        MainWindow.show()
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))

    sys.exit(app.exec())
