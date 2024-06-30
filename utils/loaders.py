import os

from PySide6 import QtCore
from PySide6.QtGui import QIcon, QPixmap

from config.cfg import EXE_DIR


def load_icon(filename: str) -> QIcon:
    """
    Load an icon from a file, resize it to 30x30 pixels, and return as a QIcon.
    :param filename: Name of the icon file
    :return: QIcon object
    """

    # Construct the full path to the icon file
    full_path = EXE_DIR + filename
    pixmap = QPixmap(full_path)
    if not pixmap.isNull():
        pixmap = pixmap.scaled(30, 30, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        return QIcon(pixmap)
    return QIcon()  # Return an empty icon if loading fails
