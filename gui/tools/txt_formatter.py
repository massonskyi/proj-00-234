from PySide6.QtWidgets import QTextEdit


class TxtFormatter:
    @classmethod
    def format_txt(cls, text_edit: QTextEdit, text: str):
        try:
            text_edit.clear()
            text_edit.append(text)
        except Exception as e:
            text_edit.clear()
            text_edit.append(f"Error processing text: {str(e)}")

    @classmethod
    def format_pdf(cls, text_edit: QTextEdit, text: str):
        try:
            text_edit.append(text)
        except Exception as e:
            text_edit.clear()
            text_edit.append(f"Error processing text: {str(e)}")