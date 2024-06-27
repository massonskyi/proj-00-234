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





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    check_configuration()
    MainWindow = Ui_StartMenu()
    MainWindow.show()
    sys.exit(app.exec())
