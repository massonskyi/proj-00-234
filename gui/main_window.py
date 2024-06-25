from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QSplitter

from gui.widgets.filemanager import FileManager
from gui.widgets.scrollcontainter import ScrollableContainer
from utils.loaders import load_icon

class Ui_MainWindow(QtWidgets.QMainWindow):
    """
    Main window class
    """
    position_widgets = {
        "menubar": [0, 0, 1, 1],
        "main_container": [0, 0, 2, 1],
        "right_toolbar": [0, 1, 2, 1]
    }

    def __init__(self, parent: QtWidgets.QWidget = None, *args, **kwargs) -> None:
        """
        Initialize the main window
        """
        super(Ui_MainWindow, self).__init__(parent)
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
        }

        self.setupUi(self, *args, **kwargs)

    def setupUi(self, _MainWindow: QtWidgets.QMainWindow, *args, **kwargs) -> None:
        _MainWindow.setObjectName("MainWindow")
        _MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(_MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.centralwidget.setLayout(self.gridLayout)
        _MainWindow.setCentralWidget(self.centralwidget)

        # Create a splitter to divide containers
        splitter = QSplitter(QtCore.Qt.Horizontal)
        self.gridLayout.addWidget(splitter, *self.position_widgets.get("main_container"))

        # Create widgets
        container = self.setupUiMainFrame()
        file_widget = FileManager(kwargs.get('path'), _MainWindow)

        file_widget.file_selected.connect(container.update_content)

        # Add widgets to splitter
        splitter.addWidget(container)
        splitter.addWidget(file_widget)

        # Right toolbar layout for buttons
        self.right_toolbar_layout = QVBoxLayout()
        self.gridLayout.addLayout(self.right_toolbar_layout, *self.position_widgets.get("right_toolbar"))

        # Button to toggle file widget visibility
        self.button_hide_file_widget = QPushButton()
        self.button_hide_file_widget.clicked.connect(self.toggle_file_widget_visibility)
        self.right_toolbar_layout.addWidget(self.button_hide_file_widget)

        self.current_icon_state = "closed"
        self.update_button_icon()

        menu_bar = self.setupUiMenu()
        _MainWindow.setMenuBar(menu_bar)
        _MainWindow.setWindowTitle("Main Window")

    def setupUiMenu(self) -> QtWidgets.QMenuBar:
        """
        Setup the main window menu
        :return: QtWidgets.QMenuBar
        """
        menubar = QtWidgets.QMenuBar(self)
        menubar.setObjectName("menubar")

        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")

        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addAction("Exit")

        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")

        return menubar

    def setupUiMainFrame(self) -> QWidget:
        """
         Setup the main frame of the main window .
        :return: QWidget
        """
        container = ScrollableContainer(data=["Open file"], file_type='text')
        container.setObjectName("MainContainer")
        return container

    def setupUiStatusBar(self, _MainWindow: QtWidgets.QStatusBar) -> None:
        pass

    def setupUiBashConsole(self, _MainWindow: QtWidgets.QMainWindow) -> None:
        pass

    def setupUiFileManager(self, _MainWindow: QtWidgets.QMainWindow) -> None:
        pass

    def setupUiTableManager(self, _MainWindow: QtWidgets.QMainWindow) -> None:
        pass

    def setupUiGraphManager(self, _MainWindow: QtWidgets.QMainWindow) -> None:
        pass

    def toggle_file_widget_visibility(self):
        """
        Toggle visibility of the file widget (FileManager)
        """
        file_widget = self.centralWidget().findChild(FileManager)
        if file_widget:
            file_widget.setVisible(not file_widget.isVisible())
            self.current_icon_state = "opened" if file_widget.isVisible() else "closed"
            self.update_button_icon()

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
