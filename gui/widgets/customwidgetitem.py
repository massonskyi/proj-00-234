from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit


class CustomWidgetItem(QWidget):
    def __init__(self, textline, parent=None):
        super().__init__(parent)
        self.include_objects = []
        self.initUI(textline)

    def initUI(self, textline):
        layout = QHBoxLayout(self)
        self.line_edit = textline
        self.include_objects.append(textline)
        layout.addWidget(self.line_edit)

    def setText(self, text):
        self.line_edit.setText(text)

    def getText(self):
        return self.line_edit.text()

    def setIcon(self, icon):
        from PySide6.QtGui import QIcon
        self.line_edit.setIcon(QIcon(icon))
        self.line_edit.setToolTip(self.line_edit.toolTip())

    def get_include_objects(self):
        return self.include_objects