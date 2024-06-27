import json
import keyword
import re

from PySide6 import QtCore
from PySide6.QtCore import Qt, QEvent, Signal
from PySide6.QtGui import QIntValidator, QPixmap, QFont, QTextCursor, QTextCharFormat, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, \
    QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView

from utils.loaders import load_icon
from utils.s2f import save_to_word, save_to_excel, save_to_pdf, save_to_csv, save_to_json, save_to_html, save_to_txt, \
    save_to_xml


class ScrollableContainer(QWidget):
    get_textboxes = Signal(list)
    show_tests = Signal(list)

    def __init__(self, data: list = None, file_type: str = None, parent=None):
        super().__init__(parent)
        self.is_show_block = False
        self.result_layout = None
        self.result_container = None
        self.icons = {
            'save_word': load_icon('./assets/save2/sword.png'),
            'save_excel': load_icon('./assets/save2/sexcel.png'),
            'save_pdf': load_icon('./assets/save2/spdf.png'),
            'save_csv': load_icon('./assets/save2/scsv.png'),
            'save_json': load_icon('./assets/save2/sjson.png'),
            'save_html': load_icon('./assets/save2/shtml.png'),
            'save_txt': load_icon('./assets/save2/stxt.png'),
            'save_xml': load_icon('./assets/save2/sxml.png'),
        }
        self.buttons_name = {
            'save_word': 'Сохранить как Word',
            'save_excel': 'Сохранить как Excel',
            'save_pdf': 'Сохранить как PDF',
            'save_csv': 'Сохранить как CSV',
            'save_json': 'Сохранить как JSON',
            'save_html': 'Сохранить как HTML',
            'save_txt': 'Сохранить как TXT',
            'save_xml': 'Сохранить как XML',
        }

        self.data = data if data else []
        self.result_data = []
        main_layout = QVBoxLayout(self)
        self.calculations = {}
        self.textboxes = []
        self.name_textboxes = []
        self.all_textboxes = []
        self.hidden_textboxes = []
        self.result_table = QTableWidget(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        if file_type == 'text':
            self.load_text_content(self.scroll_layout)
        elif file_type == 'image':
            self.load_image_content(self.scroll_layout)
        else:
            self.load_default_content(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        self.result_container = QFrame(self)
        self.result_container.setFrameShape(QFrame.StyledPanel)
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setContentsMargins(10, 10, 10, 10)
        self.result_layout.setAlignment(Qt.AlignTop)
        self.result_layout.addWidget(self.result_table)
        self.result_container.setLayout(self.result_layout)
        self.result_container.hide()

        # Connect signals for scrolling
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.check_scroll_position)

        # Add the result container to the main layout
        main_layout.addWidget(self.result_container)

        self.callbacks = {
            'save_word': save_to_word,
            'save_excel': save_to_excel,
            'save_pdf': save_to_pdf,
            'save_csv': save_to_csv,
            'save_json': save_to_json,
            'save_html': save_to_html,
            'save_txt': save_to_txt,
            'save_xml': save_to_xml,
        }

    def save(self):
        sender = self.sender()
        try:
            event = sender.objectName()
            if event in self.callbacks:
                self.callbacks[event](data=self.data, textboxes=self.all_textboxes, result_data=self.result_data)
            else:
                QMessageBox.critical(self, 'Ошибка', "ErrorKey")
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))

    def check_scroll_position(self):
        scroll_bar = self.scroll_area.verticalScrollBar()
        max_scroll = scroll_bar.maximum()
        current_scroll = scroll_bar.value()
        try:
            if current_scroll >= max_scroll:
                if not self.is_show_block:
                    self.show_result_block()
                    self.is_show_block = True
            else:
                if current_scroll == 0:
                    self.is_show_block = False
                    self.hide_result()
        except Exception as e:
            print(e)

    def show_result_block(self):
        self.result_container.show()

        self.update_result_data()

        # Display result data in table
        self.result_table.setRowCount(len(self.result_data))
        self.result_table.setColumnCount(len(self.result_data[0]) if self.result_data else 0)
        for row, row_data in enumerate(self.result_data):
            for column, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                self.result_table.setItem(row, column, item)
        self.result_table.resizeColumnsToContents()

    def hide_result(self):
        self.result_container.hide()

    def evaluate_formula(self, components):
        """Evaluate a formula by replacing placeholders with actual values."""
        components = components.split('+')
        result = 0

        try:
            for component in components:
                component = component.strip()
                found = False

                for textbox in reversed(self.textboxes):
                    if textbox.objectName() == component:
                        value = int(textbox.text()) if textbox.text().isdigit() else 0
                        result += value
                        found = True
                        break

                if not found:
                    for hidden_textbox in reversed(self.hidden_textboxes):
                        if hidden_textbox.objectName() == component:
                            if not hidden_textbox.text():  # если значение пустое, вычислить его
                                formula = next(
                                    (calc["data"].split('=')[1] for row, calc in self.calculations.items() if
                                     calc["idx"] == component),
                                    None
                                )
                                if formula:
                                    hidden_textbox.setText(str(self.evaluate_formula(formula)))
                            value = int(hidden_textbox.text()) if hidden_textbox.text().isdigit() else 0
                            result += value
                            found = True
                            break

            return result
        except Exception as e:
            print(f"Error evaluating formula: {e}")
            return 0

    def update_result_data(self):
        self.result_data = []

        for row, item in self.calculations.items():
            row_data = []
            number = item["idx"]
            indicator = item["name"]
            row_data.append(number)
            row_data.append(indicator)

            if item["data"].startswith("(Автосумма)\n"):
                formula = item["data"].split('=')[1]
                result = self.evaluate_formula(formula)
                row_data.append(str(result) if result is not None else "Ошибка")

            self.result_data.append(row_data)

    def on_text_changed(self):
        self.get_textboxes.emit(self.name_textboxes)

    def load_default_content(self, layout):
        if not self.data:
            return

        data_ptr = self.data[0].get("mdth", None)

        if not data_ptr:
            raise Exception("Не удалось получить данные")

        int_validator = QIntValidator(self)
        grid_layout = QGridLayout()
        grid_layout.setColumnStretch(1, 1)

        for row, item in enumerate(data_ptr):
            number = item["idx"]
            indicator = item["name"]

            number_label = QLabel(number)
            indicator_label = QLabel(indicator)
            indicator_label.setWordWrap(True)

            grid_layout.addWidget(number_label, row, 0)
            grid_layout.addWidget(indicator_label, row, 1)

            answer_textbox = QLineEdit()
            self.all_textboxes.append(answer_textbox)
            if number == "" or number == "№ п/п":
                answer_textbox.setObjectName(f"{number}_without_number")
            else:
                answer_textbox.setObjectName(f"{number}")
            answer_textbox.textChanged.connect(self.on_text_changed)

            if item["data"].startswith("(Автосумма)\n"):
                answer_textbox.setDisabled(True)
                self.calculations[number] = item
                self.hidden_textboxes.append(answer_textbox)
                continue

            if item["data"] != " ":
                answer_textbox.setPlaceholderText(item["data"])
                answer_textbox.setValidator(int_validator)
                answer_textbox.installEventFilter(self)
                self.name_textboxes.append([number_label, answer_textbox])
                self.textboxes.append(answer_textbox)

                grid_layout.addWidget(answer_textbox, row, 2)

        self.show_tests.emit(self.name_textboxes)
        layout.addLayout(grid_layout)

    def eventFilter(self, source, event):
        if not isinstance(event, QEvent):
            return False

        if event.type() == QtCore.QEvent.FocusIn:
            self.get_textboxes.emit(self.name_textboxes)

        if event.type() == QEvent.KeyPress and isinstance(source, QLineEdit):
            current_index = self.textboxes.index(source)

            def find_next_enabled_index(start_index, direction):
                index = start_index
                while True:
                    index = (index + direction) % len(self.textboxes)
                    if self.textboxes[index].isEnabled():
                        return index
                    if index == start_index:
                        return -1  # No enabled textbox found

            if event.key() in {Qt.Key_Return, Qt.Key_Enter, Qt.Key_Down}:
                next_index = find_next_enabled_index(current_index, 1)
                if next_index != -1:
                    self.textboxes[next_index].setFocus()
                    self.scroll_area.ensureWidgetVisible(self.textboxes[next_index])
                return True

            elif event.key() == Qt.Key_Up:
                previous_index = find_next_enabled_index(current_index, -1)
                if previous_index != -1:
                    self.textboxes[previous_index].setFocus()
                    self.scroll_area.ensureWidgetVisible(self.textboxes[previous_index])
                return True

        return super().eventFilter(source, event)

    def update_content(self, data):
        self.data = data
        self.update_ui()

    def get_data(self):
        if self.data:
            return self.data
        elif not self.data and hasattr(self, 'text_edit'):
            return self.text_edit.toPlainText()
        else:
            return None

    def update_ui(self):
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

        if not self.data:
            self.text_edit = QTextEdit()
            self.text_edit.setObjectName("base")
            self.text_edit.setReadOnly(False)
            self.text_edit.setFont(QFont("Arial", 12))
            self.text_edit.setStyleSheet(
                "QTextEdit { border: none; background-color: #f4f4f4; color: black; padding: 10px; }")
            self.scroll_layout.addWidget(self.text_edit)
            return

        if self.data and isinstance(self.data, list):
            if self.data[0] and isinstance(self.data[0], dict):
                first_key = next(iter(self.data[0].keys()))
                if first_key == 'image_path':
                    self.load_image_content(self.scroll_layout)
                elif first_key == 'mdth':
                    self.load_default_content(self.scroll_layout)
                else:
                    self.load_table_content(self.scroll_layout, self.data)
            else:
                self.load_text_content(self.scroll_layout)

    def load_text_content(self, layout):
        text_edit = QTextEdit()
        text_edit.setReadOnly(False)
        text_edit.setFont(QFont("Arial", 12))
        text_edit.setStyleSheet("QTextEdit { border: none; background-color: #f4f4f4; color: black; padding: 10px; }")

        # for item in self.data:
        #     if self.is_json(item):
        #         self.format_json(text_edit, item)
        #     elif self.is_xml(item):
        #         self.format_xml(text_edit, item)
        #     # elif self.is_python(item):
        #     #     self.format_python(text_edit, item)
        #     else:

        self.format_txt(text_edit, self.data)
        layout.addWidget(text_edit)

    def is_json(self, text):
        try:
            json.loads(text)
            return True
        except ValueError:
            return False

    def is_xml(self, text):
        import xml.etree.ElementTree as ET
        try:
            ET.fromstring(text)
            return True
        except ET.ParseError:
            return False

    # def is_python(self, text):
    #     try:
    #         compile(text, '<string>', 'exec')
    #         return True
    #     except SyntaxError:
    #         return False

    def format_json(self, text_edit, text):
        formatted_json = json.dumps(json.loads(text), indent=4)
        text_edit.append(formatted_json)

    def format_xml(self, text_edit, text):
        import xml.etree.ElementTree as ET
        try:
            tree = ET.ElementTree(ET.fromstring(text))
            formatted_xml = ET.tostring(tree.getroot(), encoding='unicode')
            text_edit.append(formatted_xml)
        except ET.ParseError as e:
            text_edit.append(f"Invalid XML: {str(e)}")

    # def format_python(self, text_edit, text):
    #     text_edit.setPlainText(text)
    #     cursor = text_edit.textCursor()
    #     cursor.select(QTextCursor.Document)
    #     cursor.setCharFormat(QTextCharFormat())
    #
    #     keywords_format = QTextCharFormat()
    #     keywords_format.setForeground(QColor("blue"))
    #     keywords_format.setFontWeight(QFont.Bold)
    #     keywords = keyword.kwlist
    #
    #     strings_format = QTextCharFormat()
    #     strings_format.setForeground(QColor("magenta"))
    #
    #     comments_format = QTextCharFormat()
    #     comments_format.setForeground(QColor("green"))
    #
    #     regex_keywords = r'\b(?:' + '|'.join(re.escape(word) for word in keywords) + r')\b'
    #     regex_strings = r'"[^"\\]*(\\.[^"\\]*)*"|\'[^\'\\]*(\\.[^\'\\]*)*\''
    #     regex_comments = r'#.*'
    #
    #     cursor.movePosition(QTextCursor.Start)
    #     while not cursor.atEnd():
    #         cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
    #         line = cursor.selectedText()
    #
    #         for match in re.finditer(regex_keywords, line):
    #             cursor.setPosition(cursor.selectionStart() + match.start())
    #             cursor.setPosition(cursor.selectionStart() + match.end(), QTextCursor.KeepAnchor)
    #             cursor.setCharFormat(keywords_format)
    #
    #         for match in re.finditer(regex_strings, line):
    #             cursor.setPosition(cursor.selectionStart() + match.start())
    #             cursor.setPosition(cursor.selectionStart() + match.end(), QTextCursor.KeepAnchor)
    #             cursor.setCharFormat(strings_format)
    #
    #         for match in re.finditer(regex_comments, line):
    #             cursor.setPosition(cursor.selectionStart() + match.start())
    #             cursor.setPosition(cursor.selectionStart() + match.end(), QTextCursor.KeepAnchor)
    #             cursor.setCharFormat(comments_format)
    #
    #         cursor.movePosition(QTextCursor.NextBlock)

    def format_txt(self, text_edit, text):
        for item in text:
            if isinstance(item, list):
                for subitem in item:
                    text_edit += str(subitem)
            text_edit.append(item)

    def load_image_content(self, layout):
        for item in self.data:
            image_label = QLabel()
            pixmap = QPixmap(item.get('image_path', ''))
            if not pixmap.isNull():
                image_label.setPixmap(pixmap.scaledToWidth(400))  # Adjust width as needed
                image_label.setAlignment(Qt.AlignCenter)
                image_label.setStyleSheet("QLabel { margin: 10px; }")
                layout.addWidget(image_label)

    def load_table_content(self, layout, data):
        if data and data[0].get('dataword', None):
            for table_data in data[0].get('dataword', None):
                table_widget = QTableWidget()
                headers = table_data[1]  # Assuming the first row is the header
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
                        item.setFlags(Qt.ItemIsEnabled)
                        table_widget.setItem(row_idx - 1, col_idx, item)  # row_idx - 1 because of skipping header

                layout.addWidget(table_widget)
            return
        if data:
            table_widget = QTableWidget()
            for row_idx, row_data in enumerate(data):
                headers = row_data.keys()
                table_widget.setColumnCount(len(headers))
                table_widget.setHorizontalHeaderLabels(headers)
                table_widget.setRowCount(len(data))

                table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                table_widget.setFont(QFont("Arial", 10))
                table_widget.setStyleSheet(
                    "QTableWidget { background-color: #f4f4f4; color: black; border: none; } QHeaderView::section { background-color: #d4d4d4; padding: 5px; border: none; } QTableWidget::item { padding: 5px; }")
                for col_idx, (col_name, col_value) in enumerate(row_data.items()):
                    item = QTableWidgetItem(str(col_value))
                    item.setFlags(Qt.ItemIsEnabled)
                    table_widget.setItem(row_idx, col_idx, item)
