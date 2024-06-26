import json
import os

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox

from gui.main_window import Ui_MainWindow


class Ui_StartMenu(QtWidgets.QWidget):
    """
    Стартовое меню с вариантами выбора.
    """

    def __init__(self) -> None:
        """
        Initializes the start menu.
        """
        super().__init__()
        self.main_window = None
        self.open_button = None
        self.file_button = None
        self.file_input = None
        self.open_project_form = None
        self.create_button = None
        self.directory_button = None
        self.directory_input = None
        self.file_type_combobox = None
        self.create_project_form = None
        self.open_project_button = None
        self.create_project_button = None
        self.setWindowTitle('Начало')
        self.setGeometry(100, 100, 400, 300)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setupUi()

    def setupUi(self) -> None:
        """
        Sets up the user interface.
        :return: None
        """
        # Create the initial layout with buttons
        initial_layout = QtWidgets.QVBoxLayout()

        self.create_project_button = QtWidgets.QPushButton("Создать новый проект")
        self.open_project_button = QtWidgets.QPushButton("Выбрать проект")

        self.create_project_button.clicked.connect(self.show_create_project_form)
        self.open_project_button.clicked.connect(self.show_open_project_form)

        initial_layout.addWidget(self.create_project_button)
        initial_layout.addWidget(self.open_project_button)

        initial_widget = QtWidgets.QWidget()
        initial_widget.setLayout(initial_layout)

        # Add the initial widget to the stacked widget
        self.stacked_widget.addWidget(initial_widget)

        # Create the create project form
        self.create_project_form = QtWidgets.QWidget()
        create_form_layout = QtWidgets.QFormLayout()
        self.directory_input = QtWidgets.QLineEdit()
        self.directory_button = QtWidgets.QPushButton("Выбрать директорию")
        self.directory_button.clicked.connect(self.select_directory)

        self.file_type_combobox = QtWidgets.QComboBox()
        self.file_type_combobox.addItems(["Все файлы (*)", "Текстовые файлы (*.txt)", "Python файлы (*.py)"])

        self.create_button = QtWidgets.QPushButton("Создать проект")
        self.create_button.clicked.connect(self.create_project_with_form)

        create_form_layout.addRow("Директория:", self.directory_input)
        create_form_layout.addRow("", self.directory_button)
        create_form_layout.addRow("Тип файла:", self.file_type_combobox)
        create_form_layout.addRow("", self.create_button)

        self.create_project_form.setLayout(create_form_layout)
        self.stacked_widget.addWidget(self.create_project_form)

        # Create the open project form
        self.open_project_form = QtWidgets.QWidget()
        open_form_layout = QtWidgets.QFormLayout()
        self.file_input = QtWidgets.QLineEdit()
        self.file_button = QtWidgets.QPushButton("Выбрать файл")
        self.file_button.clicked.connect(self.select_file)

        self.open_button = QtWidgets.QPushButton("Открыть проект")
        self.open_button.clicked.connect(self.open_project)

        open_form_layout.addRow("Файл:", self.file_input)
        open_form_layout.addRow("", self.file_button)
        open_form_layout.addRow("", self.open_button)

        self.open_project_form.setLayout(open_form_layout)
        self.stacked_widget.addWidget(self.open_project_form)

        # Set the layout for the StartMenu
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

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
                                                             "Все файлы (*);;Текстовые файлы (*.txt);;Python файлы (*.py)")
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
            if os.path.isfile(projmd_file):
                with open(projmd_file, 'r') as f:
                    project_data = json.load(f)

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
