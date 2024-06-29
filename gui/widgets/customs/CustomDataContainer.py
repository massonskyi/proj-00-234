import json
from typing import List, Any

from PySide6 import QtCore

from PySide6.QtCore import (
    Qt,
    QEvent,
    Signal
)

from PySide6.QtGui import (
    QPixmap,
    QFont
)
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QFrame,
    QGridLayout,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QPushButton
)

from gui.tools.json_formatter import JsonFormatter
from gui.tools.python_formatter import PythonFormatter
from gui.tools.txt_formatter import TxtFormatter
from gui.tools.xml_formatter import XmlFormatter
from gui.widgets.customs.CustomTextEdit import CustomTextEdit

from utils.s2f import (
    save_to_word,
    save_to_excel,
    save_to_pdf,
    save_to_csv,
    save_to_json,
    save_to_html,
    save_to_txt,
    save_to_xml
)


class CustomDataContainer(QWidget):
    """
    Custom data container for custom data
    """
    get_textboxes = Signal(list)  # list of textboxes
    show_tests = Signal(list)  # list of tests

    def __init__(self, path: str, icons: list, data: list = None, file_type: str = None, parent=None):
        """
        Initialize custom data container for custom data
        :param path: path to project path
        :param icons: list of icons for buttons
        :param data: data for custom data container
        :param file_type: file type for custom data container
        :param parent: parent widget to parent
        """
        super().__init__(parent)
        self.calculate_button = None
        self.reset_button = None
        self.scroll_layout = None
        self.scroll_content = None
        self.scroll_area = None
        self.result_table = None
        self.current_workspace = path
        self.is_show_block = False
        self.result_layout = None
        self.result_container = None
        self.icons, self.buttons_name = icons
        self.data = data if data else []
        self.result_data = []
        self.calculations = {}
        self.textboxes = []
        self.name_textboxes = []
        self.all_textboxes = []
        self.hidden_textboxes = []
        self.callbacks = self._setup_callbacks()

        self.setupUi(file_type)
        self.get_textboxes.emit(self.name_textboxes)

    def setupUi(self, file_type: str = None) -> None:
        """
        Setup the UI elements for custom data container
        :param file_type: str file type
        """
        main_layout = QVBoxLayout()

        self.result_table = QTableWidget()
        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)

        if file_type == 'text':
            self.load_text_content(self.scroll_layout)
        elif file_type == 'image':
            self.load_image_content(self.scroll_layout)
        else:
            self.load_default_content(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_content)

        self.reset_button = self._create_button('Новый файл', self.reset, False)
        self.calculate_button = self._create_button('Начать расчет', self.toggle_result_block, True)

        self.result_container = self._initalize_result_block()

        widget = QFrame()
        layout = QVBoxLayout()

        layout.addWidget(self.result_container)
        layout.addWidget(self.reset_button)

        widget.setLayout(layout)

        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(widget)

        self.scroll_area.verticalScrollBar().valueChanged.connect(self.check_scroll_position)

        self.setLayout(main_layout)

    def save(self) -> None:
        """
        Save custom data container to file system
        :return: None
        """
        sender: object = self.sender()
        self.check_main_dirs(self.current_workspace)
        try:
            event: object = sender.objectName()
            if event in self.callbacks:
                self.callbacks[event](path=self.current_workspace, data=self.data, textboxes=self.all_textboxes,
                                      result_data=self.result_data)
            else:
                QMessageBox.critical(self, 'Ошибка', "ErrorKey")
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))

    def reset(self) -> None:
        """
        Reset the custom data container
        :return: None
        """
        self.data: List = []
        self.result_data: List = []
        self.textboxes: List = []
        self.name_textboxes: List = []
        self.all_textboxes: List = []
        self.hidden_textboxes: List = []
        self.is_show_block: bool = False

        self.result_table.setVisible(False)
        self.calculate_button.setVisible(True)

        self.result_container.hide()
        self.reset_button.hide()
        self.result_table.hide()

        self.update_ui(True)
        self.scroll_area.verticalScrollBar().setValue(0)

    def check_scroll_position(self) -> None:
        """
        Check the scroll position and show the result block if needed
        :return: None
        """

        scroll_bar: QScrollArea.verticalScrollBar = self.scroll_area.verticalScrollBar()
        max_scroll: int = scroll_bar.maximum()
        current_scroll: int = scroll_bar.value()
        try:
            if current_scroll >= max_scroll:
                if self.is_show_block:
                    return

                self.show_result_block()
                self.is_show_block = True
            else:
                if current_scroll != 0:
                    return

                self.hide_result()
                self.is_show_block = False
        except Exception as e:
            print(e)

    def toggle_result_block(self) -> None:
        """
        Toggle the result block
        :return: None
        """
        if self.result_table.isVisible():
            return

        self.result_table.setVisible(True)
        self.calculate_button.hide()
        self.reset_button.setVisible(True)

        self.update_data()

    def update_data(self) -> None:
        """
        Update the data in the table in the UI
        :return: None
        """
        self.update_result_data()

        self.result_table.setRowCount(len(self.result_data))
        self.result_table.setColumnCount(len(self.result_data[0]) if self.result_data else 0)
        for row, row_data in enumerate(self.result_data):
            for column, value in enumerate(row_data):
                item: QTableWidgetItem = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.result_table.setItem(row, column, item)
        self.result_table.resizeColumnsToContents()

    def show_result_block(self) -> None:
        """
        Show the result block in the UI
        :return: None
        """
        self.result_container.show()

    def hide_result(self) -> None:
        """
        Hide the result block in the UI
        :return: None
        """
        self.result_container.hide()

    def evaluate_formula(self, components: str) -> int:
        """
        Evaluate a formula by replacing placeholders with actual values.
        :param components: str formula components
        :return: int result of formula evaluation
        """

        def get_value_from_textbox(_component: str) -> int | None:
            """
            get the value from the textbox and return the value
            :param _component: str component name or textbox name
            :return: int value of the textbox
            """
            for textbox in reversed(self.textboxes):
                if textbox.objectName() == _component:
                    return int(textbox.text()) if textbox.text().isdigit() else 0
            return None

        def get_value_from_hidden_textbox(_component: str) -> int | None:
            """
            get the value from the hidden textbox and return the value
            :param _component: str component name or textbox name
            :return: int value of the textbox
            """
            for hidden_textbox in reversed(self.hidden_textboxes):
                if hidden_textbox.objectName() == _component:
                    if not hidden_textbox.text():
                        formula = next(
                            (calc["data"].split('=')[1] for row, calc in self.calculations.items() if
                             calc["idx"] == component),
                            None
                        )
                        if formula:
                            hidden_textbox.setText(str(self.evaluate_formula(formula)))
                    return int(hidden_textbox.text()) if hidden_textbox.text().isdigit() else 0
            return None

        result: int = 0
        try:
            for component in components.split('+'):
                component: str = component.strip()
                value: int = get_value_from_textbox(component)
                if value is None:
                    value: int = get_value_from_hidden_textbox(component)
                if value is not None:
                    result += value
            return result
        except Exception as e:
            print(f"Error evaluating formula: {e}")
            return 0

    def update_result_data(self) -> None:
        """
        Update the data in the result table
        :return: None
        """
        self.result_data: list = []

        for row, item in self.calculations.items():
            row_data: list = []
            number: str = item["idx"]
            indicator: str = item["name"]
            row_data.append(number)
            row_data.append(indicator)

            if item["data"].startswith("(Автосумма)\n"):
                formula: str = item["data"].split('=')[1]
                result: int = self.evaluate_formula(formula)
                row_data.append(str(result) if result is not None else "Ошибка")

            self.result_data.append(row_data)

    def update_data_from_sender(self) -> None:
        """
        Update data from sender
        :return: None
        """

        if not self.data:
            print("No data available.")
            return

        mdth: list = self.data[0].get("mdth", None)

        if mdth is None:
            print("No 'mdth' data available.")
            return

        event: str = self.sender().objectName()
        for it in range(len(mdth)):
            if event in mdth[it]['idx']:
                mdth[it]['data'] = self.sender().text()
                break

    def on_text_changed(self) -> None:
        """
        On text changed event.
        :return: None
        """
        if not self.sender().objectName() in self.calculations.keys():
            self.update_data_from_sender()

        self.get_textboxes.emit(self.name_textboxes)

    def load_default_content(self, layout: QVBoxLayout) -> None:
        """
        Load default content to the widget.
        :param layout: QVBoxLayout layout of the widget.
        :return: None
        """
        if not self.data:
            return

        data_ptr: list = self.data[0].get("mdth", None)

        if not data_ptr:
            raise Exception("Не удалось получить данные")

        grid_layout: QGridLayout = QGridLayout()
        grid_layout.setColumnStretch(1, 1)

        for row, item in enumerate(data_ptr):
            number: str = item["idx"]
            indicator: str = item["name"]

            number_label: QLabel = QLabel(number)
            indicator_label: QLabel = QLabel(indicator)
            indicator_label.setWordWrap(True)

            grid_layout.addWidget(number_label, row, 0)
            grid_layout.addWidget(indicator_label, row, 1)

            answer_textbox: QLineEdit = QLineEdit()
            self.all_textboxes.append(answer_textbox)
            answer_textbox.setObjectName(f"{number}")

            if item["data"].startswith("(Автосумма)\n"):
                answer_textbox.setDisabled(True)
                self.calculations[number] = item
                self.hidden_textboxes.append(answer_textbox)
                continue

            if item["data"] != " ":
                try:
                    _ = int(item["data"])
                except ValueError:
                    answer_textbox.setPlaceholderText(item["data"])
                else:
                    answer_textbox.setText(item["data"])

                answer_textbox.installEventFilter(self)
                answer_textbox.textChanged.connect(self.on_text_changed)
                self.name_textboxes.append([number_label, answer_textbox])
                self.textboxes.append(answer_textbox)

                grid_layout.addWidget(answer_textbox, row, 2)

        self.show_tests.emit(self.name_textboxes)
        layout.addLayout(grid_layout)

    def set_scrollbar_value(self, obj: object) -> None:
        """
        Set the scrollbar value on object
        :param obj: object to set the scrollbar value
        :return: None
        """
        self.scroll_area.ensureWidgetVisible(obj)

    def eventFilter(self, source: QWidget, event: QEvent) -> bool | int:
        """
        Event filter for textboxes.
        :param source: QWidget source
        :param event: QEvent event
        :return: bool
        """
        if not isinstance(event, QEvent):
            return False

        if event.type() == QtCore.QEvent.Type.FocusIn:
            self.get_textboxes.emit(self.name_textboxes)

        if event.type() == QEvent.Type.KeyPress and isinstance(source, QLineEdit):
            current_index: int = self.textboxes.index(source)

            def find_next_enabled_index(start_index: int, direction: int) -> int:
                """
                find next enabled textbox index.
                """
                index: int = start_index
                while True:
                    index = (index + direction) % len(self.textboxes)
                    if self.textboxes[index].isEnabled():
                        return index
                    if index == start_index:
                        return -1  # No enabled textbox found

            if event.key() in {Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Down}:
                next_index: int = find_next_enabled_index(current_index, 1)
                if next_index != -1:
                    self.textboxes[next_index].setFocus()
                    self.scroll_area.ensureWidgetVisible(self.textboxes[next_index])
                return True

            elif event.key() == Qt.Key.Key_Up:
                previous_index: int = find_next_enabled_index(current_index, -1)
                if previous_index != -1:
                    self.textboxes[previous_index].setFocus()
                    self.scroll_area.ensureWidgetVisible(self.textboxes[previous_index])
                return True

        return super().eventFilter(source, event)

    def update_content(self, data: list) -> None:
        """
        Update the content of the widgets.
        :param data: list of dict of data
        """
        self.data: list = data
        self.update_ui()

    def get_data(self) -> list | list[Any] | None | Any:
        """
        Get data from container.
        :return: list of dict of data, else data is None, return None
        """
        if self.data:
            return self.data
        elif not self.data and hasattr(self, 'text_edit'):
            return self.text_edit.toPlainText()
        else:
            return None

    def update_ui(self, reset: bool = False) -> None:
        """
        Updates the UI with the current data.
        :param reset: If True, the data will be reset.
        :return: None
        """
        self._clear_content_block()

        if reset:
            label: QLabel = QLabel("Выберите или создайте новый файл")
            label.setFont(QFont("Arial", 16))
            self.scroll_layout.addWidget(label)
            return

        if not self.data:
            custom_text_edit: CustomTextEdit = CustomTextEdit()
            self.scroll_layout.addWidget(custom_text_edit)
            return

        if self.data and isinstance(self.data, list):
            if self.data[0] and isinstance(self.data[0], dict):
                first_key = next(iter(self.data[0].keys()))
                if first_key == 'image_path':
                    self.load_image_content(self.scroll_layout)
                elif first_key == 'mdth':
                    self.load_default_content(self.scroll_layout)
                elif first_key == 'pdf':
                    self.load_text_content(self.scroll_layout, 'pdf')
                else:
                    self.load_table_content(self.scroll_layout, self.data)
            else:
                self.load_text_content(self.scroll_layout)

    def load_text_content(self, layout: QVBoxLayout, key: str = None) -> None:
        """
        Load text content from a list of dictionaries.
        :param layout: QVBoxLayout layout to add widgets
        :param key: key of text to load from
        :return: None
        """

        def format_and_add_content(_text_edit: CustomTextEdit, _content) -> None:
            """
            Format text content and add it to layout. If key is None, add all content.
            :param _text_edit: Text edit widget
            :param _content: Text content
            :return: None
            """
            if self._is_json(_content):
                self._format_json(_text_edit, _content)
            elif self._is_xml(_content):
                self._format_xml(_text_edit, _content)
            elif self._is_python(_content):
                self._format_python(_text_edit, _content)
            else:
                self._format_txt(_text_edit, _content)

        text_edit: CustomTextEdit = CustomTextEdit()

        if key == 'pdf':
            for item in self.data[0].get('pdf'):
                TxtFormatter.format_pdf(text_edit, item)
        else:
            for item in self.data:
                if isinstance(item, list):
                    for subitem in item:
                        format_and_add_content(text_edit, subitem)
                else:
                    format_and_add_content(text_edit, item)

        text_edit.set_cursor_position(0)
        text_edit.text_edit.verticalScrollBar().setValue(0)
        layout.addWidget(text_edit)

    def _clear_content_block(self) -> None:
        """
        Clear content block.
        :return: None
        """
        for i in reversed(range(self.scroll_layout.count())):
            if isinstance(self.scroll_layout.itemAt(i), QGridLayout):
                for item in reversed(range(self.scroll_layout.itemAt(i).count())):
                    widget = self.scroll_layout.itemAt(i).itemAt(item).widget()
                    if widget:
                        widget.setParent(None)
            else:
                widget = self.scroll_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

    @staticmethod
    def _is_json(text: str) -> bool:
        """
        Check if the given text is a valid JSON.
        :param text: str text to be checked
        :return: bool True if the text is a valid JSON, False otherwise
        """
        try:
            json.loads(text)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_xml(text: str) -> bool:
        """
        Check if the given text is a valid XML.
        :param text: str text to be checked
        :return: bool True if the text is a valid XML, False otherwise
        """
        import xml.etree.ElementTree as ElementTree
        try:
            ElementTree.fromstring(text)
            return True
        except ElementTree.ParseError:
            return False

    @staticmethod
    def _is_python(text: str) -> bool:
        """
        Check if the given text is a valid Python code.
        :param text: str text to be checked
        :return: bool True if the text is a valid Python code, False otherwise
        """
        try:
            compile(text, '<string>', 'exec')
            return True
        except SyntaxError:
            return False

    @staticmethod
    def _format_json(text_edit: CustomTextEdit, text: str) -> None:
        """
        Formated and append text to container data block
        :param text_edit: CustomTextEdit text edit to format text
        :text: str text to be formatted to formatted text
        :return: None
        """
        JsonFormatter.format_json(text_edit, text)

    @staticmethod
    def _format_xml(text_edit: CustomTextEdit, text: str) -> None:
        """
        Formated and append text to container data block
        :param text_edit: CustomTextEdit text edit to format text
        :text: str text to be formatted to formatted text
        :return: None
        """
        XmlFormatter.format_xml(text_edit, text)

    @staticmethod
    def _format_python(text_edit: CustomTextEdit, text: str) -> None:
        """
        Formated and append text to container data block
        :param text_edit: CustomTextEdit text edit to format text
        :text: str text to be formatted to formatted text
        :return: None
        """
        PythonFormatter.format_python(text_edit, text)

    @staticmethod
    def _format_txt(text_edit: CustomTextEdit, text: str) -> None:
        """
        Formated and append text to container data block
        :param text_edit: CustomTextEdit text edit to format text
        :text: str text to be formatted to formatted text
        :return: None
        """
        TxtFormatter.format_txt(text_edit, text)

    def load_image_content(self, layout: QVBoxLayout) -> None:
        """
        Load data in image format in image and display on content block
        :param layout: QVBoxLayout layout to display image in content block
        """
        for item in self.data:
            image_label: QLabel = QLabel()
            pixmap: QPixmap = QPixmap(item.get('image_path', ''))
            if not pixmap.isNull():
                image_label.setPixmap(pixmap.scaledToWidth(400))  # Adjust width as needed
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                image_label.setStyleSheet("QLabel { margin: 10px; }")
                layout.addWidget(image_label)

    def load_table_content(self, layout: QVBoxLayout, data: list | dict) -> None:
        """
        Load data in table format in table and display on content block
        :param layout: QVBoxLayout layout to display table in content block
        :param data: list or dict data to display in table layout
        :return: None
        """
        if data and data[0].get('dataword', None):
            layout.addWidget(self._display_word_content(data))
        elif data:
            layout.addWidget(self._display_excel_data(data))

    @staticmethod
    def _display_word_content(data: list | dict) -> QTableWidget:
        """
        Display data in Word format
        :param data: list or dict data
        :return: QTableWidget: QTableWidget with data in Word format
        """
        table_widget: QTableWidget = QTableWidget()
        if not data:
            return table_widget

        for table_data in data[0].get('dataword', None):
            headers = table_data[1]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(table_data) - 1)  # Number of data rows excluding header
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table_widget.setFont(QFont("Arial", 10))
            table_widget.setStyleSheet(
                "QTableWidget { background-color: #f4f4f4; color: black; border: none; } "
                "QHeaderView::section { background-color: #d4d4d4; color: black; padding: 5px; border: none; } "
                "QTableWidget::item { padding: 5px; color: black;}"
            )

            for row_idx, row_data in enumerate(table_data[2:], 1):  # Start from index 1 to skip header
                for col_idx, col_value in enumerate(row_data):
                    item = QTableWidgetItem(str(col_value))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    table_widget.setItem(row_idx - 1, col_idx, item)  # row_idx - 1 because of skipping header

        return table_widget

    @staticmethod
    def _display_excel_data(data: list | dict) -> QTableWidget:
        """
        Display data in Excel format
        :param data: list or dict data
        :return: QTableWidget: QTableWidget with data in Excel format
        """
        table_widget: QTableWidget = QTableWidget()
        if not data:
            return table_widget

        for row_idx, row_data in enumerate(data):
            headers: list = row_data.keys()
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(data))

            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table_widget.setFont(QFont("Arial", 10))
            table_widget.setStyleSheet(
                """
                QTableWidget {
                    background-color: #f4f4f4;
                    color: black;
                    border: none;
                }
                QHeaderView::section {
                    background-color: #d4d4d4;
                    padding: 5px;
                    border: none;
                }
                QTableWidget::item {
                    padding: 5px;
                }
                """
            )

            for col_idx, (col_name, col_value) in enumerate(row_data.items()):
                if str(col_value) == 'nan':
                    col_value = ''
                item: QTableWidgetItem = QTableWidgetItem(str(col_value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                table_widget.setItem(row_idx, col_idx, item)

        return table_widget

    @staticmethod
    def _create_button(name: str, callback: callable = None, set_visible: bool = False) -> QPushButton:
        """
        Create button for custom data container for custom data
        :param name: string name of custom data container for custom data
        :param callback: callable callback function
        :param set_visible: bool flag for set visibility of button
        :return: QPushButton: QPushButton button for custom data container for custom data
        """
        button: QPushButton = QPushButton(name)
        button.setObjectName(name)
        button.clicked.connect(callback)
        button.setVisible(set_visible)
        return button

    def _initalize_result_block(self) -> QFrame:
        """
        Initialize result block for custom data container for custom data
        :return: QFrame: result block for custom data container for custom data container for custom data
        """
        result_container: QFrame = QFrame(self)
        result_container.setFrameShape(QFrame.StyledPanel)

        result_layout: QVBoxLayout = QVBoxLayout(result_container)

        result_layout.setContentsMargins(10, 10, 10, 10)
        result_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        result_layout.addWidget(self.calculate_button)
        result_layout.addWidget(self.result_table)

        result_container.setLayout(result_layout)
        result_container.setVisible(False)

        self.result_table.setVisible(False)
        return result_container

    @staticmethod
    def _setup_callbacks() -> dict:
        """
        Setup callbacks for custom data container for custom data
        :return: dict: callbacks for custom data container for custom data
        """
        return {
            'save_word': save_to_word,
            'save_excel': save_to_excel,
            'save_pdf': save_to_pdf,
            'save_csv': save_to_csv,
            'save_json': save_to_json,
            'save_html': save_to_html,
            'save_txt': save_to_txt,
            'save_xml': save_to_xml,
        }

    @staticmethod
    def check_main_dirs(path: str) -> None:
        """
        Check if main dirs exist in path
        """
        import os
        if not os.path.exists(f"{path}/export"):
            os.mkdir(f"{path}/export")
