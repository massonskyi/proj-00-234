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
    pixmap = QPixmap(filename)
    if not pixmap.isNull():
        return QIcon(pixmap.scaled(
            30,
            30,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        ))
    return QIcon()
