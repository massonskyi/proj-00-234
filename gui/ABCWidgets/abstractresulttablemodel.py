from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class ResultTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.headers = ["№ п/п: ", "Сумма: "]
        self.data = []  # Initialize as an empty list
        if data:
            self.parse_data(data)

    def parse_data(self, data):
        parsed_data = []
        for item in data:
            n = item.get('№ п/п')
            answer = item.get('Ответ субъекта')
            parsed_data.append((n, answer))  # Ensure it's a tuple
        self.data = parsed_data

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if not (0 <= index.row() < len(self.data) and 0 <= index.column() < len(self.headers)):
                return None
            key, value = self.data[index.row()]
            if index.column() == 0:
                return str(key)
            elif index.column() == 1:
                return str(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return None
