import sys
import os
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from utils.s2f import load_mdth_file


class FileManager(QtWidgets.QWidget):
    file_selected = Signal(list)

    def __init__(self, path: str = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('File Manager')

        # Основной макет
        layout = QtWidgets.QVBoxLayout(self)

        # Модель файловой системы
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.rootPath())

        # Дерево файловой системы
        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        if path:
            self.tree.setRootIndex(self.model.index(path))
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # Настройка отображения колонок
        self.tree.setColumnWidth(0, 250)
        self.tree.setColumnWidth(1, 100)
        self.tree.setColumnWidth(2, 100)
        self.tree.setColumnWidth(3, 150)

        # Контекстное меню
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_menu)
        self.tree.doubleClicked.connect(self.select_file)

        # Кнопки управления
        self.create_file_action = QAction("Create File", self)
        self.create_dir_action = QAction("Create Directory", self)
        self.delete_action = QAction("Delete", self)
        self.rename_action = QAction("Rename", self)

        # Слоты для кнопок
        self.create_file_action.triggered.connect(self.create_file)
        self.create_dir_action.triggered.connect(self.create_directory)
        self.delete_action.triggered.connect(self.delete_item)
        self.rename_action.triggered.connect(self.rename_item)

        # Добавление виджетов в макет
        layout.addWidget(self.tree)
        button_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(button_layout)

    def select_file(self, index):
        file_path = self.model.filePath(index)
        if file_path:
            data = []
            if file_path.lower().endswith('.mdth'):
                data = [{"mdth": load_mdth_file(file_path)}]
            elif file_path.lower().endswith(('.png', '.jpg', '.bmp')):
                data = [{'image_path': file_path}]
            else:
                with open(file_path, 'r') as f:
                    data = [line.strip() for line in f.readlines()]
            self.file_selected.emit(data)

    def open_menu(self, position):
        indexes = self.tree.selectedIndexes()
        if indexes:
            menu = QtWidgets.QMenu()
            menu.addAction(self.create_file_action)
            menu.addAction(self.create_dir_action)
            menu.addAction(self.delete_action)
            menu.addAction(self.rename_action)
            menu.exec_(self.tree.viewport().mapToGlobal(position))

    def create_file(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        dir_path = self.model.filePath(index)
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Create File", dir_path)
        if file_path:
            open(file_path, 'w').close()  # Создаем пустой файл

    def create_directory(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        dir_path = self.model.filePath(index)
        dir_name, ok = QtWidgets.QInputDialog.getText(self, "Create Directory", "Directory Name:")
        if ok and dir_name:
            os.mkdir(os.path.join(dir_path, dir_name))

    def delete_item(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        if os.path.isdir(file_path):
            os.rmdir(file_path)
        else:
            os.remove(file_path)

    def rename_item(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        new_name, ok = QtWidgets.QInputDialog.getText(self, "Rename Item", "New Name:")
        if ok and new_name:
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            os.rename(file_path, new_path)
