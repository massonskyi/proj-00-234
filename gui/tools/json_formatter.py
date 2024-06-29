import json

from PySide6.QtWidgets import QTextEdit


class JsonFormatter:
    @classmethod
    def format_json(cls, text_edit: QTextEdit, text: str):
        try:
            if isinstance(text, bytes):
                text = text.decode('utf-8')

            formatted_json = json.dumps(json.loads(text), indent=4, ensure_ascii=False)

            text_edit.clear()
            text_edit.append(formatted_json)

        except json.JSONDecodeError as e:
            text_edit.append(f"Invalid JSON data: {e}")
