import os

from PySide6 import QtCore
from PySide6.QtGui import QIcon, QPixmap


def load_icon(filename: str) -> QIcon:
    """
    Load an icon from a file, resize it to 30x30 pixels, and return as a QIcon.
    :param filename: Name of the icon file
    :return: QIcon object
    """
    # Get the directory of the current executable
    exe_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the icon file
    full_path = os.path.join(exe_dir, filename)
    pixmap = QPixmap(filename)
    if not pixmap.isNull():
        pixmap = pixmap.scaled(30, 30, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        return QIcon(pixmap)
    return QIcon()  # Return an empty icon if loading fails
