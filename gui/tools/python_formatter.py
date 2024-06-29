from PySide6.QtGui import QFont
from PySide6.QtWidgets import QTextEdit

from gui.tools.subtools.python_highlighter import PythonHighlighter


class PythonFormatter:
    @classmethod
    def format_python(cls, text_edit: QTextEdit, text: str):
        try:
            text_edit.clear()

            text_edit.setFont(QFont("Courier", 10))

            text_edit.setPlainText(text)

            cls.highlighter = PythonHighlighter(text_edit.document())

        except Exception as e:
            text_edit.clear()
            text_edit.append(f"Error processing Python code: {str(e)}")
