from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QIntValidator, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QPushButton, QGridLayout, QLineEdit, \
    QTextEdit, QHBoxLayout, QMenu, QSizePolicy, QSpacerItem, QTableView, QHeaderView


from gui.ABCWidgets.abstractresulttablemodel import ResultTableModel
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
        self.textboxes = None
        self.data = data if data else []
        self.result_data = []
        main_layout = QVBoxLayout(self)
        self.result_table_view = QTableView(self)
        self.result_model = None
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

        self.result_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.result_table_view.verticalHeader().setVisible(False)

        self.scroll_area.setWidget(self.scroll_content)

        main_layout.addWidget(self.scroll_area)

        self.additional_container = QFrame(self)
        self.additional_container.setFrameShape(QFrame.StyledPanel)
        self.additional_layout = QVBoxLayout(self.additional_container)

        self.additional_buttons_container = QFrame(self)
        self.additional_buttons_layout = QHBoxLayout(self.additional_buttons_container)
        self.additional_buttons_layout.setContentsMargins(0, 0, 0, 0)  # Ensure no extra margins

        self.add_initial_buttons()

        self.additional_layout.addWidget(self.additional_buttons_container)
        self.additional_container.hide()

        self.result_container = QFrame(self)
        self.result_container.setFrameShape(QFrame.StyledPanel)
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setContentsMargins(10, 10, 10, 10)
        self.result_layout.setAlignment(Qt.AlignTop)
        self.result_layout.addWidget(self.result_table_view)
        self.result_container.setLayout(self.result_layout)
        self.result_container.hide()

        main_layout.addWidget(self.additional_container)

        # Connect signals for scrolling
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.check_scroll_position)

        # Add the result container to the main layout
        main_layout.addWidget(self.result_container)

    def add_initial_buttons(self):
        buttons = []
        for it, (key, icon) in enumerate(self.icons.items()):
            button = QPushButton(icon, self.buttons_name.get(key))
            button.setObjectName(key)
            button.setFixedSize(175, 40)
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            button.clicked.connect(self.save)
            buttons.append(button)

            if len(buttons) <= 3:
                self.additional_buttons_layout.addWidget(button)

        if len(buttons) > 3:
            menu_button = QPushButton("...", self.additional_buttons_container)
            menu_button.setFixedSize(175, 40)
            menu_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            self.additional_buttons_layout.addWidget(menu_button)

            menu = QMenu(self)
            for button in buttons[3:]:
                action = menu.addAction(button.icon(), self.buttons_name.get(button.objectName()))
                action.setObjectName(button.objectName())
                action.triggered.connect(self.save)  # Connect the QAction's triggered signal to button's click slot

            menu_button.setMenu(menu)

        # Add spacers to ensure even distribution of buttons
        spacer_left = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        spacer_right = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.additional_buttons_layout.insertItem(0, spacer_left)
        self.additional_buttons_layout.addItem(spacer_right)
        # Add a spacer after the buttons
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.additional_buttons_layout.addItem(spacer)

    def save(self):
        sender = self.sender()
        if sender.objectName() == 'save_word':
            save_to_word(data=self.data, textboxes=self.textboxes)
        elif sender.objectName() == 'save_excel':
            save_to_excel(data=self.data, textboxes=self.textboxes)
        elif sender.objectName() == 'save_pdf':
            save_to_pdf(data=self.data, textboxes=self.textboxes)
        elif sender.objectName() == 'save_csv':
            save_to_csv(data=self.data, textboxes=self.textboxes)
        elif sender.objectName() == 'save_json':
            save_to_json(data=self.data, textboxes=self.textboxes)
        elif sender.objectName() == 'save_html':
            save_to_html(data=self.data, textboxes=self.textboxes)
        elif sender.objectName() == 'save_txt':
            save_to_txt(data=self.data, textboxes=self.textboxes)
        elif sender.objectName() == 'save_xml':
            save_to_xml(data=self.data, textboxes=self.textboxes)

    def check_scroll_position(self):
        scroll_bar = self.scroll_area.verticalScrollBar()
        max_scroll = scroll_bar.maximum()
        current_scroll = scroll_bar.value()
        try:
            if current_scroll >= max_scroll:
                if not self.is_show_block:
                    self.show_result_block()
                    self.is_show_block = True
                    self.additional_container.show()
            else:
                if current_scroll == 0:
                    self.is_show_block = False
                    self.hide_result()
                    self.additional_container.hide()
        except Exception as e:
            print(e)
    def show_result_block(self):
        # Clear existing widgets in result container
        for i in reversed(range(self.result_layout.count())):
            widget = self.result_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Prepare data for the result table view
        self.result_model = ResultTableModel(self.result_data)
        self.result_table_view.setModel(self.result_model)

        # Show the result container
        self.result_container.show()
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

    def load_default_content(self, layout):
        grid_layout = QGridLayout()
        grid_layout.setColumnStretch(1, 1)

        int_validator = QIntValidator(0, 10, self)

        self.textboxes = []

        for row, item in enumerate(self.data[0].get('mdth')):
            number, indicator, answer = item.get("№ п/п", ""), item.get("Показатель", ""), item.get("Ответ субъекта",
                                                                                                    "")
            if '(Автосумма)' in answer:
                self.result_data.append(item)
                continue

            number_label = QLabel(number)
            indicator_label = QLabel(indicator)
            answer_textbox = QLineEdit()
            answer_textbox.setObjectName(number) if number != "" else None
            answer_textbox.setPlaceholderText(answer)
            answer_textbox.setValidator(int_validator)
            answer_textbox.installEventFilter(self)

            self.textboxes.append(answer_textbox)

            number_label.setMinimumWidth(50)
            number_label.setAlignment(Qt.AlignCenter)

            indicator_label.setWordWrap(True)
            grid_layout.addWidget(number_label, row, 0)
            grid_layout.addWidget(indicator_label, row, 1)
            grid_layout.addWidget(answer_textbox, row, 2)

        layout.addLayout(grid_layout)

    def eventFilter(self, source, event):
        if not isinstance(event, QEvent):
            return

        if event.type() == QEvent.Type.KeyPress and isinstance(source, QLineEdit):
            current_index = self.textboxes.index(source)
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                next_index = (current_index + 1) % len(self.textboxes)
                self.textboxes[next_index].setFocus()
                self.scroll_area.ensureWidgetVisible(self.textboxes[next_index])
                return True

            elif event.key() == Qt.Key.Key_Up:
                next_index = (current_index - 1) % len(self.textboxes)
                if next_index < 0:
                    next_index = len(self.textboxes) - 1
                self.textboxes[next_index].setFocus()
                self.scroll_area.ensureWidgetVisible(self.textboxes[next_index])
                return True

            elif event.key() == Qt.Key.Key_Down:
                next_index = (current_index + 1) % len(self.textboxes)
                self.textboxes[next_index].setFocus()
                self.scroll_area.ensureWidgetVisible(self.textboxes[next_index])
                return True

            elif event.key() == Qt.Key.Key_Up and event.modifiers() == Qt.ControlModifier:
                self.parentWidget().focusPreviousChild()
                return True

            elif event.key() == Qt.Key.Key_Down and event.modifiers() == Qt.ControlModifier:
                self.parentWidget().focusNextChild()
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
