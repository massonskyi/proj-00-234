from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, \
    QAbstractItemView, QTableWidgetItem, QLineEdit


class CustomTestWidget(QWidget):
    set_scrollbar_value = Signal(QLineEdit)

    def __init__(self, test_names=None, icons=None, parent=None):
        super().__init__(parent)
        if icons is None:
            icons = []

        if test_names is None:
            test_names = []

        self.tests = test_names
        self.icons = icons
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.table_widget = QTableWidget()
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.table_widget.setColumnCount(1)
        self.table_widget.setHorizontalHeaderLabels(['Questions'])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addWidget(self.table_widget)

        self.test_items = []

        for name in self.test_items:
            self.addTestItem(name)

    def addTestItem(self, name):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        text_item = QTableWidgetItem()
        text_item.setText(name.text())
        text_item.setIcon(QIcon(self.icons[1]))
        self.table_widget.setItem(row_position, 0, text_item)

    def loadTests(self, tests: list):
        self.table_widget.setRowCount(0)  # Clear existing rows
        self.test_items = tests
        for name, _ in self.test_items:
            self.addTestItem(name)

    def on_cell_double_clicked(self, row, column):
        if not hasattr(self, 'label_to_textbox_map'):
            return

        item = self.table_widget.item(row, column)
        if item:
            var = self.label_to_textbox_map[item.text()]
            var.setFocus(Qt.FocusReason.OtherFocusReason)
            self.set_scrollbar_value.emit(var)

    @Slot(list)
    def updateIcons(self, data):
        self.label_to_textbox_map = {label.text(): textbox for label, textbox in data}
        for row in range(self.table_widget.rowCount()):
            icon_item = self.table_widget.item(row, 0)
            if icon_item.text() in self.label_to_textbox_map:
                if self.is_test_done(self.label_to_textbox_map[icon_item.text()]):
                    icon_item.setIcon(QIcon(self.icons[0]))  # Done icon
                elif self.is_test_in_progress(self.label_to_textbox_map[icon_item.text()]):
                    icon_item.setIcon(QIcon(self.icons[2]))  # Not done icon
                else:
                    icon_item.setIcon(QIcon(self.icons[1]))  # In-progress icon

    def is_test_done(self, test_name: QLineEdit):
        if test_name:
            return test_name.text() != ''

    def is_test_in_progress(self, test_name: QLineEdit):
        if test_name:
            return test_name.hasFocus()
