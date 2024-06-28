import json
import os

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QMainWindow, QWidget

from gui.main_window import Ui_MainWindow
from gui.widgets.customtitlebar import CustomTitleBar
from utils.loaders import load_icon



class Ui_StartMenu(QMainWindow):
    """
    Стартовое меню с вариантами выбора.
    """

    def __init__(self) -> None:
        """
        Initializes the start menu.
        """
        super().__init__()
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
        self.setGeometry(100, 100, 400, 300)
        self.stacked_widget = QtWidgets.QStackedWidget()

        self.icons = {
            'hidden_folder': load_icon('./assets/folder/hidden_folder.png'),
            'open_clear_folder': load_icon('./assets/folder/open_clear_folder.png'),
            'open_full_folder': load_icon('./assets/folder/open_full_folder.png'),
            'bash': load_icon('./assets/console/bash.png'),
            'py': load_icon('./assets/console/py.png'),
            'test_btn': load_icon('./assets/test/button.png'),
            'success_question': load_icon('./assets/test/qs.png'),
            'failed_question': load_icon('./assets/test/qc.png'),
            'process_question': load_icon('./assets/test/qp.png'),
            'menu_exit': load_icon('./assets/main/menu_exit.png'),
            'menu_file': load_icon('./assets/main/menu_file.png'),
            'menu_new': load_icon('./assets/main/menu_new.png'),
            'menu_new_file': load_icon('./assets/main/menu_new_file.png'),
            'menu_new_project': load_icon('./assets/main/menu_new_project.png'),
            'menu_open': load_icon('./assets/main/menu_open.png'),
            'menu_open_file': load_icon('./assets/main/menu_open_file.png'),
            'menu_open_project': load_icon('./assets/main/menu_open_project.png'),
            'menu_save': load_icon('./assets/main/menu_save.png'),
            'menu_save_as': load_icon('./assets/main/menu_save_as.png'),
            'menu_txt': load_icon('./assets/main/menu_txt.png'),
            'main_menu': load_icon('./assets/main/main_menu.png'),
            'button': load_icon('./assets/default/button.png'),
            'minimize': load_icon('./assets/title/minimize.png'),
            'maximize': load_icon('./assets/title/maximize.png'),
            'close': load_icon('./assets/title/close.png'),
            'title_main': load_icon('./assets/title_main.png'),
        }

        self.setupUi()

    def setupUi(self) -> None:
        central_widget = QWidget()
        self.setWindowTitle('project-00-234')
        self.setGeometry(100, 100, 400, 800)

        self.create_project_button = self.create_button("Создать новый проект", self.show_create_project_form,
                                                        "#4CAF50")
        self.create_project_button.setFixedWidth(200)
        self.open_project_button = self.create_button("Выбрать проект", self.show_open_project_form,
                                                      "#008CBA")
        self.open_project_button.setFixedWidth(200)
        self.exit_button = self.create_button("Выход", self.close_window, "#5a9c9b")
        self.exit_button.setFixedWidth(200)
        initial_layout = QtWidgets.QVBoxLayout()
        initial_layout.addWidget(self.create_project_button, alignment=QtCore.Qt.AlignCenter)  # Center align button
        initial_layout.addWidget(self.open_project_button, alignment=QtCore.Qt.AlignCenter)  # Center align button
        initial_layout.addWidget(self.exit_button, alignment=QtCore.Qt.AlignCenter)  # Center align button

        initial_widget = QtWidgets.QWidget()
        initial_widget.setLayout(initial_layout)
        self.stacked_widget.addWidget(initial_widget)

        self.setup_create_project_form()
        self.setup_open_project_form()

        main_layout = QtWidgets.QVBoxLayout()
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

    def check_main_dirs(self, path):
        import os
        if not os.path.exists(f"{path}/export"):
            os.mkdir(f"{path}/export")

    def create_project(self, dir_path, file_type="*") -> None:
        """
        Creates a project directory and saves project information to a .projmd file.
        :param dir_path: Directory path for the project.
        :param file_type: Selected file type for the project.
        :return: None
        """
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        project_data = {
            "directory": dir_path,
            "file_type": file_type
        }

        projmd_file = os.path.join(dir_path, "proj.projmd")
        with open(projmd_file, 'w') as f:
            json.dump(project_data, f, indent=4)

        from utils.configuration_config_mdt import ConfigurationMDTH
        try:
            ConfigurationMDTH.create_configuration_config_mdt(dir_path).save_as_json()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        else:
            print("Configuration file created successfully.")
        self.check_main_dirs(dir_path)
        if file_type:
            self.open_main_window(dir_path, file_type)

    def open_project(self) -> None:
        """
        Opens the main window for an existing project by selecting the project directory.
        :return: None
        """
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбрать директорию проекта для открытия")
        if dir_path:
            projmd_file = os.path.join(dir_path, "proj.projmd")
            config_file = os.path.join(dir_path, "configuration_config_mdt.json")
            if os.path.exists(projmd_file):
                with open(projmd_file, 'r') as f:
                    project_data = json.load(f)
            else:
                project_data = {
                    "directory": dir_path,
                    "file_type": "*"
                }

                with open(projmd_file, 'w') as f:
                    json.dump(project_data, f, indent=4)

            if not os.path.exists(config_file):
                from utils.configuration_config_mdt import ConfigurationMDTH
                try:
                    ConfigurationMDTH.create_configuration_config_mdt(dir_path).save_as_json()
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))
                    return
            self.check_main_dirs(dir_path)
            if os.path.exists(projmd_file) and os.path.exists(config_file):
                self.open_main_window(project_data['directory'], project_data.get('file_type'))

    def open_main_window(self, project_path, file_type=None) -> None:
        """
        Opens the main window.
        :param project_path: The path to the project.
        :param file_type: The file type.
        :return: None
        """
        self.main_window = Ui_MainWindow(**{'path': project_path, 'ft': file_type})
        self.main_window.show()
        self.close()