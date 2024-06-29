from PySide6.QtGui import (
    QFont,
    QTextCursor
)
from PySide6.QtWidgets import (
    QWidget,
    QTextEdit,
    QHBoxLayout
)

from gui.widgets.customs.CustomLineNumberArea import CustomLineNumberArea


class CustomTextEdit(QWidget):
    """
    Custom text edit widget with line number area
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize custom text edit widget with line number area
        """
        super().__init__(*args, **kwargs)

        self.text_edit = self._create_text_edit()
        self.line_number_area = self._create_line_number_area()

        self.update_line_numbers()

        self.text_edit.textChanged.connect(self.update_line_numbers)
        self.text_edit.verticalScrollBar().valueChanged.connect(self.sync_scroll)

        self.setLayout(self._create_layout(self, self.line_number_area, self.text_edit))

    def update_line_numbers(self) -> None:
        """
        Update line number area with custom text edit widget content
        """
        line_count: int = self.text_edit.document().blockCount()
        line_numbers: str = "\n".join(map(str, range(1, line_count + 1)))
        self.line_number_area.setPlainText(line_numbers)

    def append(self, _text: str) -> None:
        """
        Append text to text edit widget content
        :param _text: text to append to text edit widget
        """
        self.text_edit.append(_text)
        self.update_line_numbers()

    def sync_scroll(self) -> None:
        """
        Sync scroll bar of line number area with text edit widget
        """
        value: int = self.text_edit.verticalScrollBar().value()
        self.line_number_area.update_scroll(value)

    def set_cursor_position(self, _position: int) -> None:
        """
        Set cursor position of text edit widget content
        :param _position: cursor position of text edit widget content
        """
        cursor: QTextCursor = self.text_edit.textCursor()
        cursor.setPosition(_position)
        self.text_edit.setTextCursor(cursor)

    def clear(self) -> None:
        """
        Clear text edit widget content  and set cursor position to 0
        """
        self.text_edit.clear()
        self.update_line_numbers()
        cursor: QTextCursor = self.text_edit.textCursor()
        cursor.setPosition(0)
        self.text_edit.setTextCursor(cursor)

    @staticmethod
    def _create_text_edit() -> QTextEdit:
        """
        Create custom text edit widget with line number area
        :return QTextEdit: custom text edit widget with line number area
        """
        text_edit: QTextEdit = QTextEdit()
        text_edit.setObjectName("base")
        text_edit.setReadOnly(False)
        text_edit.setFont(QFont("Arial", 12))
        text_edit.setStyleSheet(
            "QTextEdit { border: none; background-color: #f4f4f4; color: black; }")
        return text_edit

    @staticmethod
    def _create_line_number_area() -> CustomLineNumberArea:
        """
        Create custom line number area with custom text edit widget with line number area
        :return CustomLineNumberArea: custom line number area with custom text edit widget with line number area
        """
        line_number_area: CustomLineNumberArea = CustomLineNumberArea()
        line_number_area.setFont(QFont("Courier New", 12))
        return line_number_area

    @staticmethod
    def _create_layout(obj: QWidget, line_number_area: CustomLineNumberArea, text_edit: QTextEdit) -> QHBoxLayout:
        """
        Create custom layout with custom text edit widget with line number area and custom text edit widget with line number area
        :param obj: custom text edit widget with line number area and custom text edit widget with line number area
        :param line_number_area: custom line number area with custom text edit widget with line number area
        :param text_edit: custom text edit widget with line number area
        :return QHBoxLayout: custom layout with custom text edit widget with line number area and custom text edit widget with line number area
        """
        layout: QHBoxLayout = QHBoxLayout(obj)
        layout.addWidget(line_number_area)
        layout.addWidget(text_edit)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout
