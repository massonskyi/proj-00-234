from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QIntValidator, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, \
    QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox

from utils.loaders import load_icon
from utils.s2f import save_to_word, save_to_excel, save_to_pdf, save_to_csv, save_to_json, save_to_html, save_to_txt, \
    save_to_xml


class ScrollableContainer(QWidget):
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
            self.callbacks[sender.objectName()](data=self.data, textboxes=self.textboxes, result_data=self.result_data)
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
        # for textbox in self.textboxes:
        #     if not textbox.text().strip():
        #         return

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

    def load_text_content(self, layout):
        text_edit = QTextEdit()
        for item in self.data:
            text_edit.append(item)
        layout.addWidget(text_edit)

    def load_image_content(self, layout):
        for item in self.data:
            image_label = QLabel()
            pixmap = QPixmap(item.get('image_path', ''))
            if not pixmap.isNull():
                image_label.setPixmap(pixmap.scaledToWidth(400))  # Adjust width as needed
                layout.addWidget(image_label)

    def evaluate_formula(self, components):
        """Evaluate a formula by replacing placeholders with actual values."""
        components = components.split('+')
        result = 0

        try:
            for component in components:
                component = component.strip()

                # Проверка в видимых текстовых полях
                for textbox in reversed(self.textboxes):
                    if textbox.objectName() == component:
                        value = int(textbox.text())
                        result += value
                        break
                else:
                    # Проверка в скрытых текстовых полях
                    for hidden_textbox in self.hidden_textboxes:
                        if hidden_textbox.objectName() == component:
                            if not hidden_textbox.text():  # если значение пустое, вычислить его
                                formula = (calc["data"].split('=')[1] for row, calc in self.calculations.items() if
                                           calc["idx"] == component)
                                if formula:
                                    hidden_textbox.setText(str(self.evaluate_formula(formula)))
                            value = int(hidden_textbox.text())
                            result += value
                            break
            return result
        except Exception as e:
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
        """Handler for text changes in textboxes."""
        for textbox in self.textboxes:
            if not textbox.text():
                return

        self.update_result_data()

    def load_default_content(self, layout):
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
            answer_textbox.setText("1")
            answer_textbox.setPlaceholderText(item["data"])
            answer_textbox.setValidator(int_validator)
            answer_textbox.installEventFilter(self)

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
                grid_layout.addWidget(answer_textbox, row, 2)
                self.textboxes.append(answer_textbox)

        layout.addLayout(grid_layout)

    def eventFilter(self, source, event):
        if not isinstance(event, QEvent):
            return False

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

        if self.data and isinstance(self.data, list):
            if self.data[0] and isinstance(self.data[0], dict):
                first_key = next(iter(self.data[0].keys()))
                if first_key == 'image_path':
                    self.load_image_content(self.scroll_layout)

                if first_key == 'mdth':
                    self.load_default_content(self.scroll_layout)
            else:
                self.load_text_content(self.scroll_layout)
