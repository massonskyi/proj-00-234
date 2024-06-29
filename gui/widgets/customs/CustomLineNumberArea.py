from PySide6.QtGui import (
    QFont,
    Qt,
    QResizeEvent
)
from PySide6.QtWidgets import QPlainTextEdit


class CustomLineNumberArea(QPlainTextEdit):
    """
    Class to handle the line number area
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialise the class of the line number area
        """
        super().__init__(*args, **kwargs)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #e0e0e0; color: #555555;padding-left: 5px;")
        self.setFont(QFont("Courier New", 12))
        self.setFixedWidth(65)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def update_scroll(self, value: int) -> None:
        """
        Update the scroll bar
        :return: None
        """
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(value)

    def update_line_number_area(self, value: int) -> None:
        """
        Update the line number area
        :return: None
        """
        self.setPlainText(str(value))

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Resize the line number area
        :return: None
        """
        super().resizeEvent(event)
