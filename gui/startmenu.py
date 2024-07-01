import json
import os

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QMessageBox, QMainWindow, QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout

from gui.Threads.LoadThread import LoaderThread
from gui.main_window import Ui_MainWindow
from gui.widgets.customs.CustomLoadingWindow import LoadingWindow
from utils.loaders import load_icon
from utils.s2f import check_main_dirs
from utils.tools import check_configuration, remove_pycache_dirs


class Ui_StartMenu(QMainWindow):
    """
    Стартовое меню с вариантами выбора.
    """

    def __init__(self, assets: dict) -> None:
        """
        Initializes the start menu.
        """
        super().__init__()
        # self.setWindowFlags(Qt.FramelessWindowHint)  # Remove the default title bar
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self._run_setup()
        self.title_bar = None
        self.setMaximumWidth(600)
        self.setMaximumHeight(800)
        self.main_window = None
        self.open_button = None
        self.file_button = None
        self.file_input = None
        self.open_project_form = None
        self.directory_button = None
        self.directory_input = None
        self.file_type_combobox = None
        self.create_project_form = None
        self.open_project_button = None
        self.create_project_button = None
        self.setWindowTitle('Начало')
        self.center()
        self.resize(650, 500)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.assets = assets
        self.icons = assets.get('icons')

        self.setupUi()

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def setupUi(self):
        central_widget = QWidget()
        self.setWindowTitle('project-00-234')

        # Left image
        image_label = QLabel()
        pixmap = QtGui.QPixmap(self.icons.get('start_screen_pixmap'))  # Replace with the path to your image
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setFixedSize(300, 600)

        # Buttons
        self.create_project_button = self.create_button("Создать новый проект", self.show_create_project_form,
                                                        "#4CAF50")
        self.create_project_button.setFixedWidth(200)
        self.open_project_button = self.create_button("Выбрать проект", self.show_open_project_form, "#008CBA")
        self.open_project_button.setFixedWidth(200)
        self.exit_button = self.create_button("Выход", self.close_window, "#5a9c9b")
        self.exit_button.setFixedWidth(200)

        initial_layout = QVBoxLayout()
        initial_layout.addWidget(self.create_project_button, alignment=QtCore.Qt.AlignCenter)
        initial_layout.addWidget(self.open_project_button, alignment=QtCore.Qt.AlignCenter)
        initial_layout.addWidget(self.exit_button, alignment=QtCore.Qt.AlignCenter)

        initial_widget = QWidget()
        initial_widget.setLayout(initial_layout)
        self.stacked_widget.addWidget(initial_widget)

        self.setup_create_project_form()
        self.setup_open_project_form()

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(image_label)
        main_layout.addWidget(self.stacked_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def close_window(self) -> None:
        self.close()

    def create_button(self, text, on_click, color=None) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(on_click)
        if color:
            button.setStyleSheet(f"background-color: {color}; color: white;")
        button.setIcon(self.icons.get('button'))  # Replace "icon.png" with your icon file path
        button.setIconSize(QtCore.QSize(24, 24))  # Adjust icon size as needed
        button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        return button

    def setup_create_project_form(self) -> None:
        self.create_project_form = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()

        self.directory_input = self.setup_line_edit()
        self.directory_button = self.create_button("Выбрать директорию", self.select_directory, "#008CBA")

        self.file_type_combobox = QtWidgets.QComboBox()
        self.file_type_combobox.addItems(["Все файлы (*)", "Текстовые файлы (*.txt)", "Python файлы (*.py)"])

        self.create_project_button = self.create_button("Создать проект", self.create_project_with_form, "#618578")
        back_button = self.create_button("Назад", self.back_to_start_form, "#746185")

        layout.addRow("Директория:", self.directory_input)
        layout.addRow("", self.directory_button)
        layout.addRow("Тип файла:", self.file_type_combobox)
        layout.addRow("", self.create_project_button)
        layout.addRow("", back_button)

        self.create_project_form.setLayout(layout)
        self.stacked_widget.addWidget(self.create_project_form)

    def setup_open_project_form(self) -> None:
        self.open_project_form = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()

        self.file_input = self.setup_line_edit()
        self.open_button = self.create_button("Открыть проект", self.open_project, "#008CBA")
        back_button = self.create_button("Назад", self.back_to_start_form, "#746185")

        layout.addRow("Файл:", self.file_input)
        layout.addRow("", self.open_button)
        layout.addRow("", back_button)

        self.open_project_form.setLayout(layout)
        self.stacked_widget.addWidget(self.open_project_form)

    def setup_line_edit(self) -> QtWidgets.QLineEdit:
        line_edit = QtWidgets.QLineEdit()
        line_edit.setReadOnly(True)
        return line_edit

    def show_create_project_form(self) -> None:
        """
        Shows the create project form.
        :return: None
        """
        self.stacked_widget.setCurrentWidget(self.create_project_form)

    def show_open_project_form(self) -> None:
        """
        Shows the open project form.
        :return: None
        """
        self.stacked_widget.setCurrentWidget(self.open_project_form)

    def back_to_start_form(self) -> None:
        """
        Navigates back to the start menu.
        :return: None
        """
        self.stacked_widget.setCurrentIndex(0)

    def select_directory(self) -> None:
        """
        Selects a directory and sets the text of the directory input.
        :return: None
        """
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбрать директорию для нового проекта")
        if dir_path:
            self.directory_input.setText(dir_path)

    def select_file(self) -> None:
        """
        Selects a file and sets the text of the file input.
        :return: None
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать проект", "",
                                                             "Все файлы (*.mdth)")
        if file_path:
            self.file_input.setText(file_path)
            self.open_main_window(file_path)

    def create_project_with_form(self) -> None:
        """
        Creates the project form.
        :return: None
        """
        dir_path = self.directory_input.text()
        # file_type = self.file_type_combobox.currentText(encoding="utf-8")

        if dir_path:
            self.create_project(dir_path)

    def create_project(self, dir_path, file_type="*") -> None:
        """
        Creates a project directory and saves project information to a .projmd file.
        :param dir_path: Directory path for the project.
        :param file_type: Selected file type for the project.
        :return: None
        """
        from utils.s2f import create_project

        res, err = create_project(dir_path, file_type)
        if err:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать проект\n{err}")
            return

        check_main_dirs(dir_path)
        if file_type:
            self.open_main_window(dir_path, file_type)

    def open_project(self) -> None:
        """
        Opens the main window for an existing project by selecting the project directory.
        :return: None
        """
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбрать директорию проекта для открытия")
        if dir_path:
            from utils.s2f import open_project
            project_data, err = open_project(dir_path)
            if err:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть проект\n{err}")
                return

            check_main_dirs(dir_path)
            self.open_main_window(project_data['directory'], project_data.get('file_type'))

    def open_main_window(self, project_path: str, file_type: str = None, from_file: bool = False) -> None:
        """
        Opens the main window.
        :param project_path: The path to the project.
        :param file_type: The file type.
        :param from_file: Whether the main window is from file or from main window.
        :return: None
        """
        self.main_window = Ui_MainWindow(assets=self.assets.copy(), **{'path': project_path, 'ft': file_type})
        if from_file:
            from utils.s2f import open_project
            project_data, err = open_project(project_path)
            if err:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть проект\n{err}")
                return
            check_main_dirs(project_path)
            self.main_window.load_open_file_signal.emit(project_path)

        self.main_window.show()

        if self.isVisible():
            self.close()
            self.assets = None

    def _run_setup(self) -> None:
        self._thread_check_configuration()

    def _thread_check_configuration(self) -> None:
        """
        Checks if the configuration file exists and creates it if it doesn't.
        :return: None
        """
        self.loader_window = LoadingWindow(self)  # Create instance of LoadingWindow
        self.loader_window.setWindowModality(Qt.WindowModal)
        self.loader_window.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.loader_window.show()
        self.loader_thread = LoaderThread(check_configuration)
        self.loader_thread.progress_update.connect(self.loader_window.update_progress)
        self.loader_thread.task_completed.connect(self.on_check_configuration_completed)
        self.loader_thread.start()

    def _thread_remove_cache_dirs(self) -> None:
        """
        Removes the cache directory from the main window.
        :return: None
        """
        self.loader_window = LoadingWindow(self)  # Create instance of LoadingWindow
        self.loader_window.setWindowModality(Qt.WindowModal)
        self.loader_window.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.loader_window.show()
        self.loader_thread = LoaderThread(remove_pycache_dirs)
        self.loader_thread.progress_update.connect(self.loader_window.update_progress)
        self.loader_thread.task_completed.connect(self.on_remove_cache_dirs_completed)
        self.loader_thread.start()

    def on_remove_cache_dirs_completed(self):
        self.loader_window.close()

    def on_check_configuration_completed(self):
        self.loader_window.close()
        self._thread_remove_cache_dirs()
