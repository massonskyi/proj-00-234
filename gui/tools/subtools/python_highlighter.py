from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import Qt, QRegularExpression


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000FF"))
        keyword_format.setFontWeight(QFont.Bold)

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#008000"))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#808080"))
        comment_format.setFontItalic(True)

        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#A020F0"))

        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
            'except', 'False', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try',
            'while', 'with', 'yield'
        ]

        self.rules = []

        keyword_patterns = [QRegularExpression(r'\b' + keyword + r'\b') for keyword in keywords]
        for pattern in keyword_patterns:
            self.rules.append((pattern, keyword_format))

        self.rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        self.rules.append((QRegularExpression(r'#[^\n]*'), comment_format))

        self.rules.append((QRegularExpression(r'\b[A-Za-z_][A-Za-z0-9_]*(?=\()'), function_format))

    def highlightBlock(self, text):
        for pattern, format in self.rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)