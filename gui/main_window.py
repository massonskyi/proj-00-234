import os
import subprocess
import sys

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QSplitter, QFrame, QHBoxLayout, QFileDialog, \
    QMessageBox

from gui.tools.subtools.graph_window import GraphWindow
from gui.widgets.customs.CustomBashConsole import CustomBashConsole
from gui.widgets.customs.CustomDataContainer import CustomDataContainer
from gui.widgets.customs.CustomFileManager import CustomFileManager
from gui.widgets.customs.CustomGraphWidget import CustomGraphWidget
from gui.widgets.customs.CustomPyConsole import CustomPyConsole
from gui.widgets.customs.CustomTestWidget import CustomTestWidget
from gui.widgets.customs.CustomTitleBar import CustomTitleBar
from utils.s2f import check_main_dirs


class Ui_MainWindow(QtWidgets.QMainWindow):
    """
    Main window class
    """

    _change_directory_signal = QtCore.Signal(str)
    _load_open_file_signal = QtCore.Signal(str)

    position_widgets = {
        "title_bar": [0, 0, 1, 2],
        "main_container": [1, 1, 2, 1],
        "right_toolbar": [1, 2, 2, 1],
        "left_toolbar": [1, 0],
    }

    def __init__(self, assets: dict, parent: QtWidgets.QWidget = None, *args, **kwargs) -> None:
        """
        Initialize the main window
        """
        super(Ui_MainWindow, self).__init__(parent)
        self.graph_window = None
        self.graph_widget_grapf_fucntion_button = None
        self.graph_widget_histogram_btn = None
        self.test_widget = None
        self.graph_box_widget = None
        self.left_toolbar_splitter = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.icons = assets.get("icons", {})
        self.graph_widget = None
        self.button_graph_toggle = None
        self.right_container = None
        self.button_test = None
        self.button_pyconsole = None
        self.button_bash = None
        self.left_layout = None
        self.saves_icons = assets.get("saves_icons", {}).copy()
        self.buttons_name = assets.get("btn_names", {}).copy()
        self.splitter_block = None

        self.splitter = None
        self.left_container = None
        self.current_workspace = kwargs.get("path")
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
        self.current_open_file = ''
        self.setupUi(self, *args, **kwargs)
        callbacks = self.configureCallbacks()
        self.title_bar = CustomTitleBar(saves_icons=self.saves_icons, icons=self.icons, callbacks=callbacks,
                                        parent=self)
        self.setMenuWidget(self.title_bar)

    def configureCallbacks(self) -> dict:
        callbacks = {
            'new_file': self.new_file,
            'open_file': self.open_file,
            'save_file': self.save_file,
            'new_project': self.new_project,
            'open_project': self.open_project,
            'new_py_file': self.new_python_file,
            'new_txt_file': self.new_plain_text,
            'save': self.container.save,
            'close': self.close,
            'open_file_explorer': self.open_file_explorer,
            'open_project_explorer': self.open_project
        }
        return callbacks

    @property
    def change_directory_signal(self) -> QtCore.Signal:
        """
        Get the signal to change the directory
        """
        return self._change_directory_signal

    @property
    def load_open_file_signal(self) -> QtCore.Signal:
        """
        Get the signal to load the open file
        """
        return self._load_open_file_signal

    def setupUi(self, _MainWindow: QtWidgets.QMainWindow, *args, **kwargs) -> None:
        _MainWindow.setObjectName("MainWindow")
        _MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(_MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.container: CustomDataContainer = self.setupUiMainFrame()
        self.bash_console = CustomBashConsole(self.current_workspace, self.container)
        self.bash_console.setVisible(False)

        python_installed = self.check_python_installed()

        if python_installed:
            self.pyconsole = CustomPyConsole(self.current_workspace, self.container)
            self.pyconsole.setVisible(False)
        else:
            self.pyconsole = None
            QMessageBox.warning(self, "Python is not installed",
                                "Python не обнаружен, некоторый функционал ограничен.\n\n")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)

        self.centralwidget.setLayout(self.gridLayout)
        _MainWindow.setCentralWidget(self.centralwidget)

        # Create a splitter to divide containers
        self.splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
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
        self.left_toolbar_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Buttons for toggling visibility
        self.button_hide_file_widget = QPushButton()
        self.button_hide_file_widget.setObjectName("hide_file_widget_btn")
        self.button_hide_file_widget.setFixedSize(50, 40)
        self.button_hide_file_widget.clicked.connect(self.toggle_buttons_widget_visibility)
        self.button_hide_file_widget.setToolTip("Toggle File Widget")
        self.button_hide_file_widget.setStyleSheet(
            """
            background-color: #f0d1f5;
            """
        )

        self.button_bash = QPushButton(icon=self.icons.get('bash'))
        self.button_bash.setObjectName("hide_bash_widget_btn")
        self.button_bash.setFixedSize(50, 40)
        self.button_bash.clicked.connect(self.toggle_buttons_widget_visibility)
        self.button_bash.setToolTip("Toggle Bash Console")
        self.button_bash.setStyleSheet(
            """
            background-color: #dbf5ba;
            """
        )

        self.button_pyconsole = QPushButton(icon=self.icons.get('py'))
        self.button_pyconsole.setObjectName("hide_pyconsole_widget_btn")
        self.button_pyconsole.setFixedSize(50, 40)
        self.button_pyconsole.clicked.connect(self.toggle_buttons_widget_visibility)
        self.button_pyconsole.setToolTip("Toggle Python Console")
        self.button_pyconsole.setStyleSheet(
            """
            background-color: #dbf5ba;
            """
        )

        self.button_test = QPushButton(icon=self.icons.get('test_btn'))
        self.button_test.setObjectName("hide_test_widget_btn")
        self.button_test.setFixedSize(50, 40)
        self.button_test.clicked.connect(self.toggle_buttons_widget_visibility)
        self.button_test.setToolTip("Toggle tests")
        self.button_test.setStyleSheet(
            """
            background-color: #dbf5ba;
            """
        )

        self.button_graph_toggle = QPushButton(icon=self.icons.get('graph'))
        self.button_graph_toggle.setObjectName("toggle_graph_btn")
        self.button_graph_toggle.setFixedSize(50, 40)
        self.button_graph_toggle.clicked.connect(self.toggle_buttons_widget_visibility)
        self.button_graph_toggle.setToolTip("Toggle graph")
        self.button_graph_toggle.setStyleSheet(
            """
            background-color: #dbf5ba;
            """
        )

        if not python_installed:
            self.button_pyconsole.setEnabled(False)

        # Add buttons to the toolbar layout
        self.left_toolbar_layout.addWidget(self.button_hide_file_widget)
        self.left_toolbar_layout.addWidget(self.button_test)
        self.left_toolbar_layout.addWidget(self.button_graph_toggle)

        self.left_toolbar_layout.addStretch()
        self.left_toolbar_layout.addWidget(self.button_pyconsole)
        self.left_toolbar_layout.addWidget(self.button_bash)

        self.left_toolbar_splitter = QSplitter(QtCore.Qt.Orientation.Vertical)
        self.test_widget = CustomTestWidget(icons=[self.icons.get('success_question'),
                                                   self.icons.get('failed_question'),
                                                   self.icons.get('process_question')],
                                            parent=self.left_container)
        self.test_widget.setVisible(False)

        self.graph_widget = CustomGraphWidget(parent=self.left_container)
        self.graph_widget.mouseDoubleClickEvent = self.graph_double_click_event

        self.graph_widget_histogram_btn = QPushButton(icon=self.icons.get('bar_chart'))
        self.graph_widget_histogram_btn.setObjectName("graph_widget_histogram_btn")
        self.graph_widget_histogram_btn.setFixedSize(50, 40)
        self.graph_widget_histogram_btn.clicked.connect(self.draw_histogram)
        self.graph_widget_histogram_btn.setToolTip("Toggle File Widget")
        self.graph_widget_histogram_btn.setStyleSheet(
            """
            background-color: #dbf5ba;
            """
        )
        self.graph_widget_grapf_fucntion_button = QPushButton(icon=self.icons.get('function_f_graph'))
        self.graph_widget_grapf_fucntion_button.setObjectName("graph_widget_grapf_fucntion_button")
        self.graph_widget_grapf_fucntion_button.setFixedSize(50, 40)
        self.graph_widget_grapf_fucntion_button.clicked.connect(self.draw_graph)
        self.graph_widget_grapf_fucntion_button.setToolTip("Toggle File Widget")
        self.graph_widget_grapf_fucntion_button.setStyleSheet(
            """
            background-color: #dbf5ba;
            """
        )
        self.test_widget.set_scrollbar_value.connect(self.container.set_scrollbar_value)
        self.container.send_values.connect(self.graph_widget.plot_histogram)
        self.container.get_textboxes.connect(self.test_widget.updateIcons)
        self.container.show_tests.connect(self.test_widget.loadTests)

        self.file_widget = CustomFileManager(kwargs.get('path'), _MainWindow)

        self.file_widget.file_selected.connect(self.container.update_content)
        self.file_widget.filepath_selected.connect(self.update_current_open_file)
        self.change_directory_signal.connect(self.file_widget.change_directory)
        self.load_open_file_signal.connect(self.file_widget.load_file)
        self.container.need_to_reset.connect(lambda: self.file_widget.load_file(self.current_open_file))

        self.graph_box_widget = QWidget()
        layout = QHBoxLayout(self.graph_box_widget)
        btn_widget = QWidget()
        btn_layout = QVBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        btn_layout.addWidget(self.graph_widget_histogram_btn)
        btn_layout.addWidget(self.graph_widget_grapf_fucntion_button)
        layout.addWidget(btn_widget)
        layout.addWidget(self.graph_widget)
        self.graph_box_widget.setVisible(False)

        self.left_toolbar_splitter.addWidget(self.file_widget)
        self.left_toolbar_splitter.addWidget(self.test_widget)
        self.left_toolbar_splitter.addWidget(self.graph_box_widget)

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
        self.right_toolbar_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
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
        self.splitter_console = QSplitter(QtCore.Qt.Orientation.Horizontal)
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
        self.splitter_block = QSplitter(QtCore.Qt.Orientation.Vertical)
        self.splitter_block.addWidget(self.splitter)
        self.splitter_block.addWidget(console_widget)

        self.gridLayout.addWidget(self.splitter_block, 0, 0, 1, 1)

        self.adjust_container_sizes_()

        _MainWindow.setWindowTitle("Main Window")

    def draw_histogram(self):
        self.container.send_values.disconnect()
        self.container.send_values.connect(self.graph_widget.plot_histogram)
        self.container.resend_data()

    def draw_graph(self):
        self.container.send_values.disconnect()
        self.container.send_values.connect(self.graph_widget.plot)
        self.container.resend_data()

    def check_python_installed(self):
        try:
            subprocess.check_output(['python', '--version'])
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.title_bar.hide_file_path_label()

    def open_file_explorer(self, path=None):
        if not path:
            path = self.current_workspace
        print(f"Opening file explorer with path:  {path}")
        if not os.path.exists(path):
            print(f"Path does not exist: {path}")
            return

        try:
            if sys.platform.startswith('win'):
                print(f"Opening explorer with path: {path}")
                subprocess.Popen(['explorer', path], shell=True)
            elif sys.platform.startswith('linux'):
                print(f"Opening xdg-open with path: {path}")
                subprocess.Popen(['xdg-open', path], shell=True)
            else:
                raise NotImplementedError("Unsupported operating system")
        except Exception as e:
            print(f"Failed to open file explorer: {e}")

    def setupUiMainFrame(self) -> CustomDataContainer:
        """
         Setup the main frame of the main window .
        :return: QWidget
        """
        container = CustomDataContainer(self.current_workspace, [self.saves_icons, self.buttons_name])
        container.setObjectName("MainContainer")
        return container

    def setupUiStatusBar(self, _MainWindow: QtWidgets.QStatusBar) -> None:
        pass

    def update_current_open_file(self, filepath):
        self.current_open_file = filepath
        self.title_bar.update_current_open_file(filepath)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_S:
            self.save_file()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        self.save_file()
        event.accept()

    def save_file(self):
        file_path = self.current_open_file
        if not file_path:
            return

        if file_path.endswith(".mdth"):
            import json
            try:
                with open(self.current_open_file, "r", encoding="utf-8") as f:
                    data_file = json.load(f)

                for it, (data_idx, data_ptr) in enumerate(zip(data_file, self.container.all_textboxes)):
                    if data_ptr.text().isdigit() or data_ptr.text() != '':
                        data_idx['data'] = data_ptr.text()

                with open(self.current_open_file, "w", encoding="utf-8") as f:
                    json.dump(data_file, f, ensure_ascii=False, indent=4)

                print("Data saved successfully.")
            except Exception as e:
                print(f"Failed to save data: {e}")
            return
        if file_path.endswith((".txt", ".py", ".json")):
            with open(file_path, 'w') as f:
                text = self.container.get_data()
                if not text:
                    QMessageBox.information(self, "File saved failed", "File not is saved, please save it manually")
                f.write(text)
            return
        else:
            QMessageBox.information(self, "File saved failed", "File type is not supported")

    def toggle_buttons_widget_visibility(self) -> None:
        """
        Toggle the visibility of the buttons widget.
        :return: None
        """

        def toggle_visibility(_widget: QWidget, _button: QPushButton, _widget_name: str) -> None:
            """
            Toggle the visibility of the buttons widget.
            :param: _widget: QWidget
            :param: _button: QPushButton
            :param: _widget_name: str
            :return: None
            """
            if _widget:
                visible: bool = not _widget.isVisible()
                button_styleSheet: str = "background-color: #f0d1f5;" if visible else "background-color: #dbf5ba;"
                _widget.setVisible(visible)
                _button.setStyleSheet(button_styleSheet)

            if _widget_name in ['hide_file_widget_btn', 'hide_test_widget_btn', 'toggle_graph_btn']:
                self.adjust_container_sizes()
                if _widget_name == 'toggle_graph_btn' and _widget.isVisible:
                    self.container.resend_data()
                elif _widget_name == 'toggle_graph_btn' and not _widget.isVisible:
                    self.graph_widget.clear()
            elif _widget_name in ['show_file_widget_btn', 'show_test_widget_btn']:
                self.adjust_container_sizes_()

        widget_name: str = self.sender().objectName()
        widget_mapping = {
            "hide_file_widget_btn": (self.file_widget, self.button_hide_file_widget),
            "hide_test_widget_btn": (self.test_widget, self.button_test),
            "hide_bash_widget_btn": (self.bash_console, self.button_bash),
            "hide_pyconsole_widget_btn": (self.pyconsole, self.button_pyconsole),
            "toggle_graph_btn": (self.graph_box_widget, self.button_graph_toggle),
        }

        widget, button = widget_mapping.get(widget_name, (None, None))
        toggle_visibility(widget, button, _widget_name=widget_name)

    def adjust_container_sizes_(self):
        if self.pyconsole:
            if self.bash_console.isVisible() and self.pyconsole.isVisible():
                self.splitter_console.setSizes(
                    [int(0.5 * self.splitter_console.width()), int(0.5 * self.splitter_console.width())])
                self.splitter_block.setSizes(
                    [int(0.7 * self.splitter_console.width()), int(0.3 * self.splitter_console.width())])
            elif self.bash_console.isVisible():
                self.splitter_console.setSizes([int(1.0 * self.splitter_console.width()), 0])
                self.splitter_block.setSizes(
                    [int(0.7 * self.splitter_console.width()), int(0.3 * self.splitter_console.width())])
            elif self.pyconsole.isVisible():
                self.splitter_console.setSizes([0, int(1.0 * self.splitter_console.width())])
                self.splitter_block.setSizes(
                    [int(0.7 * self.splitter_console.width()), int(0.3 * self.splitter_console.width())])
            else:
                self.splitter_console.setSizes([0, 0])
                self.splitter_block.setSizes([int(1.0 * self.splitter_console.width()), 0])
        else:
            if self.bash_console.isVisible():
                self.splitter_console.setSizes(
                    [int(0.5 * self.splitter_console.width()), int(0.5 * self.splitter_console.width())])
                self.splitter_block.setSizes(
                    [int(0.7 * self.splitter_console.width()), int(0.3 * self.splitter_console.width())])
            elif self.bash_console.isVisible():
                self.splitter_console.setSizes([int(1.0 * self.splitter_console.width()), 0])
                self.splitter_block.setSizes(
                    [int(0.7 * self.splitter_console.width()), int(0.3 * self.splitter_console.width())])
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
                with open(f"{os.path.join(os.path.dirname(file_path), 'configuration_config_mdt.json')}", "r",
                          encoding="utf-8") as file:
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
                from utils.s2f import create_project

                res, err = create_project(directory_path)
                if err:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось создать проект\n{err}")
                    return

                check_main_dirs(directory_path)

                from utils.s2f import open_project
                project_data, err = open_project(directory_path)
                if err:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось открыть проект\n{err}")
                    return

                self.change_directory_signal.emit(directory_path)
                self.current_workspace = directory_path
                self.title_bar.update_current_workspace(directory_path)
                QMessageBox.information(self, "Success", f"New project created: {directory_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create project: {str(e)}")

    def new_python_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Create New Python File", "", "Python Files (*.py)",
                                                   options=options)
        if file_path:
            try:
                with open(file_path + ".py", 'w') as file:
                    file.write('')
                QMessageBox.information(self, "Success", f"New Python file created: {file_path}.py")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create Python file: {str(e)}")

    def new_plain_text(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Create New Plain Text File", "", "Text Files (*.txt)",
                                                   options=options)
        if file_path:
            try:
                with open(file_path + '.txt', 'w') as file:
                    file.write('')
                QMessageBox.information(self, "Success", f"New plain text file created: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create plain text file: {str(e)}")

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
        if file_path:
            try:
                self.load_open_file_signal.emit(file_path)
                from utils.s2f import copy_file
                res, err = copy_file(file_path, self.current_workspace)
                if err:
                    QMessageBox.critical(self, "Error", f"Failed to copy file: {str(err)}")
                    return

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")

    def open_project(self):
        directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбрать директорию проекта для открытия")
        if directory_path:
            from utils.s2f import open_project
            project_data, err = open_project(directory_path)
            if err:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть проект\n{err}")
                return

            check_main_dirs(directory_path)
            self.change_directory_signal.emit(directory_path)
            self.current_workspace = directory_path
            self.title_bar.update_current_workspace(directory_path)

    def reset(self, path=None):
        self.file_widget = CustomFileManager(path, self)
        self.container.reset()

    def graph_double_click_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_graph_in_new_window()

    def open_graph_in_new_window(self):
        # Remove from main window
        self.graph_box_widget.setParent(None)

        # Create and show the new graph window
        self.graph_window = GraphWindow(self.graph_box_widget, self)
        self.graph_window.show()

    def _add_graph(self):
        # Restore graph widget to the main window
        self.graph_box_widget.setParent(None)  # Remove from any current parent
        self.left_toolbar_splitter.addWidget(self.graph_box_widget)
