from PySide6 import QtCore
from PySide6.QtGui import QIcon, QPixmap


def load_icon(filename: str) -> QIcon:
    """
    Load an icon from a file, resize it to 30x30 pixels, and return as a QIcon.
    :param filename: Name of the icon file
    :return: QIcon object
    """
    pixmap = QPixmap(filename)
    if not pixmap.isNull():
        pixmap = pixmap.scaled(75, 75, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        return QIcon(pixmap)
    return QIcon()  # Return an empty icon if loading fails
