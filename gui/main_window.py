import os
import subprocess
import sys
import PySide6
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QSplitter, QFrame, QHBoxLayout, QFileDialog, \
    QMessageBox

from gui.widgets.filemanager import FileManager
from gui.widgets.scrollcontainter import ScrollableContainer
from gui.widgets.testwidget import TestWidget
from utils.loaders import load_icon
from utils.s2f import save_to_word
from gui.widgets.pyconsole import ConsoleWidget
from gui.widgets.bashconsole import BashConsoleWidget


class Ui_MainWindow(QtWidgets.QMainWindow):
    """
    Main window class
    """
    position_widgets = {
        "main_container": [0, 1, 2, 1],
        "right_toolbar": [0, 2, 2, 1],
        "left_toolbar": [0, 0],
    }

    def __init__(self, parent: QtWidgets.QWidget = None, *args, **kwargs) -> None:
        """
        Initialize the main window
        """
        super(Ui_MainWindow, self).__init__(parent)
        self.bash_console = None
        self.pyconsole = None
        self.splitter_console = None
        self.right_toolbar_container = None
        self.left_toolbar_container = None
        self.file_widget = None
        self.container = None
        self.left_toolbar_layout = None
        self.current_icon_state = None
        self.button_hide_file_widget = None
        self.right_toolbar_layout = None
        self.gridLayout = None
        self.centralwidget = None
        self.assets_path = "./assets"

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
        }

        self.saves_icons = {
            'save_word': load_icon('./assets/save2/sword.png'),
            'save_excel': load_icon('./assets/save2/sexcel.png'),
            'save_pdf': load_icon('./assets/save2/spdf.png'),
            'save_csv': load_icon('./assets/save2/scsv.png'),
            'save_json': load_icon('./assets/save2/sjson.png'),
            'save_html': load_icon('./assets/save2/shtml.png'),
            'save_txt': load_icon('./assets/save2/stxt.png'),
            'save_xml': load_icon('./assets/save2/sxml.png'),
        }
        self.buttons_name = {
            'save_word': 'Сохранить как Word',
            'save_excel': 'Сохранить как Excel',
            'save_pdf': 'Сохранить как PDF',
            'save_csv': 'Сохранить как CSV',
            'save_json': 'Сохранить как JSON',
            'save_html': 'Сохранить как HTML',
            'save_txt': 'Сохранить как TXT',
            'save_xml': 'Сохранить как XML',
        }
        self.current_open_file  = None
        self.setupUi(self, *args, **kwargs)

    def setupUi(self, _MainWindow: QtWidgets.QMainWindow, *args, **kwargs) -> None:
        _MainWindow.setObjectName("MainWindow")
        _MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(_MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.container = self.setupUiMainFrame()
        self.bash_console = BashConsoleWidget(self.container)

        python_installed = self.check_python_installed()

        if python_installed:
            self.pyconsole = ConsoleWidget(self.container)
            self.pyconsole.setVisible(False)
        else:
            self.pyconsole = None

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)

        self.centralwidget.setLayout(self.gridLayout)
        _MainWindow.setCentralWidget(self.centralwidget)

        # Create a splitter to divide containers
        self.splitter = QSplitter(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet("""
              QSplitter::handle {
                  background: lightgray;
              }
          """)

        # Create left container that includes the file manager and left toolbar
        self.left_container = QWidget()
        self.left_layout = QHBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)

        # Left toolbar with buttons
        self.left_toolbar_container = QFrame(self.left_container)
        self.left_toolbar_container.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.left_toolbar_container.setFixedWidth(50)
        self.left_toolbar_container.setMaximumWidth(50)

        self.left_toolbar_layout = QVBoxLayout(self.left_toolbar_container)
        self.left_toolbar_layout.setContentsMargins(0, 0, 0, 0)
        self.left_toolbar_layout.setSpacing(0)
        self.left_toolbar_layout.setAlignment(QtCore.Qt.AlignTop)

        # Buttons for toggling visibility
        self.button_hide_file_widget = QPushButton()
        self.button_hide_file_widget.setFixedSize(50, 40)
        self.button_hide_file_widget.clicked.connect(self.toggle_file_widget_visibility)
        self.button_hide_file_widget.setToolTip("Toggle File Widget")

        self.button_bash = QPushButton(icon=self.icons.get('bash'))
        self.button_bash.setFixedSize(50, 40)
        self.button_bash.clicked.connect(self.toggle_bash_widget_visibility)
        self.button_bash.setToolTip("Toggle Bash Console")

        self.button_pyconsole = QPushButton(icon=self.icons.get('py'))
        self.button_pyconsole.setFixedSize(50, 40)
        self.button_pyconsole.clicked.connect(self.toggle_pyconsole_widget_visibility)
        self.button_pyconsole.setToolTip("Toggle Python Console")

        self.button_test = QPushButton(icon=self.icons.get('test_btn'))
        self.button_test.setFixedSize(50, 40)
        self.button_test.clicked.connect(self.toggle_tests_widget_visibility)
        self.button_test.setToolTip("Toggle tests")

        if not python_installed:
            self.button_pyconsole.setEnabled(False)

        # Add buttons to the toolbar layout
        self.left_toolbar_layout.addWidget(self.button_hide_file_widget)
        self.left_toolbar_layout.addWidget(self.button_bash)
        self.left_toolbar_layout.addWidget(self.button_pyconsole)
        self.left_toolbar_layout.addWidget(self.button_test)

        # Create splitter for FileManager and TestWidget
        self.left_toolbar_splitter = QSplitter(QtCore.Qt.Vertical)
        self.test_widget = TestWidget(icons=[self.icons.get('success_question'),
                                             self.icons.get('failed_question'),
                                             self.icons.get('process_question')],
                                      parent=self.left_container)

        self.container.get_textboxes.connect(self.test_widget.updateIcons)
        self.container.show_tests.connect(self.test_widget.loadTests)
        self.file_widget = FileManager(kwargs.get('path'), _MainWindow)
        self.file_widget.file_selected.connect(self.container.update_content)
        self.file_widget.filepath_selected.connect(self.update_current_open_file)

        # Add FileManager and TestWidget to the splitter
        self.left_toolbar_splitter.addWidget(self.file_widget)
        self.left_toolbar_splitter.addWidget(self.test_widget)

        # Add splitter and left toolbar container to the left layout
        self.left_layout.addWidget(self.left_toolbar_container)
        self.left_layout.addWidget(self.left_toolbar_splitter)

        self.right_container = QWidget()
        self.right_layout = QHBoxLayout(self.right_container)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        self.right_toolbar_container = QFrame(self.right_container)
        self.right_toolbar_container.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.right_toolbar_layout = QVBoxLayout(self.right_toolbar_container)
        self.right_toolbar_layout.setContentsMargins(0, 0, 0, 0)
        self.right_toolbar_layout.setSpacing(0)
        self.right_toolbar_layout.setAlignment(QtCore.Qt.AlignTop)
        self.right_toolbar_container.setFixedWidth(60)

        self.right_layout.addWidget(self.container)
        self.right_layout.addWidget(self.right_toolbar_container)

        self.splitter.addWidget(self.left_container)
        self.splitter.addWidget(self.right_container)
        self.splitter.setSizes([int(0.20 * self.splitter.width()), int(0.80 * self.splitter.width())])
        self.add_initial_buttons()
        self.current_icon_state = "closed"
        self.update_button_icon()

        # Create a separate splitter for the consoles
        self.splitter_console = QSplitter(QtCore.Qt.Horizontal)
        self.splitter_console.addWidget(self.bash_console)
        if python_installed:
            self.splitter_console.addWidget(self.pyconsole)

        console_widget = QWidget()
        console_layout = QHBoxLayout(console_widget)
        console_layout.setContentsMargins(0, 0, 0, 0)
        console_layout.setSpacing(0)
        console_layout.addWidget(self.splitter_console)
        console_widget.setLayout(console_layout)

        # Create a vertical splitter that contains both the main content and the consoles
        self.splitter_block = QSplitter(QtCore.Qt.Vertical)
        self.splitter_block.addWidget(self.splitter)
        self.splitter_block.addWidget(console_widget)

        self.gridLayout.addWidget(self.splitter_block, 0, 0, 1, 1)

        self.adjust_container_sizes_()

        menu_bar = self.setupUiMenu()
        _MainWindow.setMenuBar(menu_bar)
        _MainWindow.setWindowTitle("Main Window")

    def check_python_installed(self):
        try:
            subprocess.check_output(['python', '--version'])
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False

    def setupUiMenu(self) -> QtWidgets.QMenuBar:
        """
        Setup the main window menu
        :return: QtWidgets.QMenuBar
        """

        def configure_menu(menubar: QtWidgets.QMenuBar) -> None:
            # New submenu
            new_menu = QtWidgets.QMenu("New", self)
            new_file_action = QAction("New File", self)
            new_file_action.triggered.connect(self.new_file)
            new_project_action = QAction("New Project", self)
            new_project_action.triggered.connect(self.new_project)
            new_python_action = QAction("New Python File", self)
            new_python_action.triggered.connect(self.new_python_file)
            new_plain_text_action = QAction("New Plain Text", self)
            new_plain_text_action.triggered.connect(self.new_plain_text)
            new_menu.addAction(new_file_action)
            new_menu.addAction(new_project_action)
            new_menu.addSeparator()
            new_menu.addAction(new_python_action)
            new_menu.addAction(new_plain_text_action)

            # Open submenu
            open_menu = QtWidgets.QMenu("Open", self)
            open_file_action = QAction("Open File", self)
            open_project_action = QAction("Open Project", self)
            open_menu.addAction(open_file_action)
            open_menu.addAction(open_project_action)

            save_menu = QtWidgets.QMenu("Save As", self)
            save_to_word_action = QAction(text="docx", icon=self.saves_icons['save_word'], parent=self)
            save_to_word_action.setObjectName("save_to_word")
            save_to_word_action.triggered.connect(self.container.save)

            save_to_excel_action = QAction(text="xlsx", icon=self.saves_icons['save_excel'], parent=self)
            save_to_excel_action.setObjectName("save_to_excel")
            save_to_excel_action.triggered.connect(self.container.save)

            save_to_pdf_action = QAction(text="pdf", icon=self.saves_icons['save_pdf'], parent=self)
            save_to_pdf_action.setObjectName("save_to_pdf")
            save_to_pdf_action.triggered.connect(self.container.save)

            save_to_csv_action = QAction(text="csv", icon=self.saves_icons['save_csv'], parent=self)
            save_to_csv_action.setObjectName("save_to_csv")
            save_to_csv_action.triggered.connect(self.container.save)

            save_to_json_action = QAction(text="json", icon=self.saves_icons['save_json'], parent=self)
            save_to_json_action.setObjectName("save_to_json")
            save_to_json_action.triggered.connect(self.container.save)

            save_to_html_action = QAction(text="html", icon=self.saves_icons['save_html'], parent=self)
            save_to_html_action.setObjectName("save_to_html")
            save_to_html_action.triggered.connect(self.container.save)

            save_to_xml_action = QAction(text="xml", icon=self.saves_icons['save_xml'], parent=self)
            save_to_xml_action.setObjectName("save_to_xml")
            save_to_xml_action.triggered.connect(self.container.save)

            save_to_txt_action = QAction(text="txt", icon=self.saves_icons['save_txt'], parent=self)
            save_to_txt_action.setObjectName("save_to_txt")
            save_to_txt_action.triggered.connect(self.container.save)

            save_menu.addAction(save_to_word_action)
            save_menu.addAction(save_to_excel_action)
            save_menu.addAction(save_to_pdf_action)
            save_menu.addAction(save_to_csv_action)
            save_menu.addAction(save_to_json_action)
            save_menu.addAction(save_to_html_action)
            save_menu.addAction(save_to_xml_action)
            save_menu.addAction(save_to_txt_action)

            file_menu = menubar.addMenu("File")
            file_menu.addMenu(new_menu)
            file_menu.addMenu(open_menu)
            file_menu.addAction("Save")
            file_menu.addMenu(save_menu)
            file_menu.addAction("Exit")

            # Edit menu
            edit_menu = menubar.addMenu("Edit")
            edit_menu.addAction("Undo")
            edit_menu.addAction("Redo")
            edit_menu.addAction("Cut")
            edit_menu.addAction("Copy")
            edit_menu.addAction("Paste")

        menubar = QtWidgets.QMenuBar(self)
        menubar.setObjectName("menubar")

        configure_menu(menubar)

        return menubar

    def setupUiMainFrame(self) -> QWidget:
        """
         Setup the main frame of the main window .
        :return: QWidget
        """
        container = ScrollableContainer()
        container.setObjectName("MainContainer")
        return container

    def setupUiStatusBar(self, _MainWindow: QtWidgets.QStatusBar) -> None:
        pass

    def update_current_open_file(self, filepath):
        self.current_open_file =filepath

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_S:
            self.save_file()
        else:
            super().keyPressEvent(event)

    def save_file(self):
        file_path = self.current_open_file
        if file_path:
            with open(file_path, 'w') as f:
                text = self.container.get_data()
                if not text:
                    QMessageBox.information(self, "File saved failed", "File not is saved, please save it manually")
                    return

                f.write(text)

    def toggle_file_widget_visibility(self):
        file_widget = self.file_widget
        if file_widget:
            file_visible = not file_widget.isVisible()
            file_widget.setVisible(file_visible)
            self.adjust_container_sizes()

    def toggle_tests_widget_visibility(self):
        file_widget = self.test_widget
        if file_widget:
            file_visible = not file_widget.isVisible()
            file_widget.setVisible(file_visible)
            self.adjust_container_sizes()

    def toggle_bash_widget_visibility(self):
        file_widget = self.bash_console
        if file_widget:
            file_visible = not file_widget.isVisible()
            file_widget.setVisible(file_visible)
            self.adjust_container_sizes_()

    def toggle_pyconsole_widget_visibility(self):
        file_widget = self.pyconsole
        if file_widget:
            file_visible = not file_widget.isVisible()
            file_widget.setVisible(file_visible)
            self.adjust_container_sizes_()

    def adjust_container_sizes_(self):
        if self.bash_console.isVisible() and self.pyconsole.isVisible():
            self.splitter_console.setSizes(
                [int(0.5 * self.splitter_console.width()), int(0.5 * self.splitter_console.width())])
            self.splitter_block.setSizes([int(0.7 * self.splitter_console.width()), int(0.3 * self.splitter_console.width())])
        elif self.bash_console.isVisible():
            self.splitter_console.setSizes([int(1.0 * self.splitter_console.width()), 0])
            self.splitter_block.setSizes([int(0.7 * self.splitter_console.width()), int(0.3 * self.splitter_console.width())])
        elif self.pyconsole.isVisible():
            self.splitter_console.setSizes([0, int(1.0 * self.splitter_console.width())])
            self.splitter_block.setSizes([int(0.7 * self.splitter_console.width()), int(0.3 * self.splitter_console.width())])
        else:
            self.splitter_console.setSizes([0, 0])
            self.splitter_block.setSizes([int(1.0 * self.splitter_console.width()), 0])

    def adjust_container_sizes(self):
        if not self.file_widget.isVisible() and not self.test_widget.isVisible():
            self.splitter.setSizes([int(0.02 * self.splitter.width()), int(0.95 * self.splitter.width())])
        else:
            self.splitter.setSizes([int(0.20 * self.splitter.width()), int(0.80 * self.splitter.width())])

    def update_button_icon(self):
        """
        Update button icon based on current state
        """
        if self.current_icon_state == "closed":
            self.button_hide_file_widget.setIcon(self.icons["hidden_folder"])
        elif self.current_icon_state == "opened":
            self.button_hide_file_widget.setIcon(self.icons["open_full_folder"])
        elif self.current_icon_state == "empty_directory":
            self.button_hide_file_widget.setIcon(self.icons["open_clear_folder"])
        else:
            self.button_hide_file_widget.setIcon(QtGui.QIcon())  # Default icon if state not recognized

    def add_initial_buttons(self):
        buttons = []
        for it, (key, icon) in enumerate(self.saves_icons.items()):
            button = QPushButton(icon, "")
            button.setObjectName(key)
            button.setFixedSize(50, 40)
            button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
            button.clicked.connect(self.container.save)
            button.setToolTip(self.buttons_name.get(key))  # Set tooltip with the button name
            buttons.append(button)

            if len(buttons) <= 3:
                self.right_toolbar_layout.addWidget(button)

        if len(buttons) > 3:
            menu_button = QPushButton("...", self.right_toolbar_container)
            menu_button.setFixedSize(50, 40)
            menu_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
            self.right_toolbar_layout.addWidget(menu_button)

            menu = QtWidgets.QMenu(self)
            for button in buttons[3:]:
                action = menu.addAction(button.icon(), self.buttons_name.get(button.objectName()))
                action.setObjectName(button.objectName())
                action.triggered.connect(self.container.save)

            menu_button.setMenu(menu)

    def new_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Create New File", "", "All Files (*.mdth)", options=options)
        if file_path:
            try:
                import json
                with open("configuration_config_mdt.json", "r", encoding="utf-8") as file:
                    data = json.load(file)

                from utils.s2f import generate_mdth_file

                if sys.platform.startswith("win"):
                    generate_mdth_file(data, file_path)
                if sys.platform.startswith("lin"):
                    generate_mdth_file(data, file_path + ".mdth")

                QMessageBox.information(self, "Success", f"New file created: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")

    def new_project(self):
        options = QFileDialog.Options()
        directory_path = QFileDialog.getExistingDirectory(self, "Create New Project", options=options)
        if directory_path:
            try:
                os.makedirs(directory_path, exist_ok=True)
                QMessageBox.information(self, "Success", f"New project created: {directory_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create project: {str(e)}")

    def new_python_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Create New Python File", "", "Python Files (*.py)",
                                                   options=options)
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write('')
                QMessageBox.information(self, "Success", f"New Python file created: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create Python file: {str(e)}")

    def new_plain_text(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Create New Plain Text File", "", "Text Files (*.txt)",
                                                   options=options)
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write('')
                QMessageBox.information(self, "Success", f"New plain text file created: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create plain text file: {str(e)}")

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
        if file_path:
            # Open the file (implementation dependent on your application)
            QMessageBox.information(self, "File Opened", f"File opened: {file_path}")

    def open_project(self):
        options = QFileDialog.Options()
        directory_path = QFileDialog.getExistingDirectory(self, "Open Project", options=options)
        if directory_path:
            # Open the project (implementation dependent on your application)
            QMessageBox.information(self, "Project Opened", f"Project opened: {directory_path}")
