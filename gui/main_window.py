import sys

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QWidget

from gui.widgets.bashconsole import BashConsoleWidget


class Ui_MainWindow(QtWidgets.QMainWindow):
    """
    Main window class
    """
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """
        Initialize the main window
        """
        super(Ui_MainWindow, self).__init__(parent)
        self.left_dock = None
        self.status_bar = None
        self.console_output = None
        self.content_area = None
        self.main_layout = None
        self.file_button = None
        self.project_button = None
        self.nav_layout = None
        self.nav_bar = None
        self.menu_file = None
        self.menu_bar = None
        self.central_layout = None
        self.centralwidget = None
        self.setupUi(self)

    def setupUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        """
        Setup the main window
        :param MainWindow: QMainWindow instance
        :return: None
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.central_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Menu bar
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_file = self.menu_bar.addMenu("Меню")
        self.menu_bar.setObjectName("menu_bar")
        MainWindow.setMenuBar(self.menu_bar)

        # Navigation bar
        self.nav_bar = QtWidgets.QWidget(self.centralwidget)
        self.nav_layout = QtWidgets.QHBoxLayout(self.nav_bar)
        self.nav_bar.setLayout(self.nav_layout)

        self.project_button = QtWidgets.QPushButton("NameProject", self.nav_bar)
        self.file_button = QtWidgets.QPushButton("file", self.nav_bar)

        self.nav_layout.addWidget(self.project_button)
        self.nav_layout.addWidget(self.file_button)

        self.central_layout.addWidget(self.nav_bar)

        # Main layout
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Content area
        self.content_area = QtWidgets.QWidget(self.centralwidget)
        self.content_area.setObjectName("content_area")
        self.content_area.setStyleSheet("background-color: lightgrey;")
        self.main_layout.addWidget(self.content_area, 0, 1, 1, 1)

        self.central_layout.addLayout(self.main_layout)

        # Console output area
        self.console_output = BashConsoleWidget()
        self.console_output.setObjectName("console_output")
        self.console_output.setPlaceholderText(f"{sys.platform}, {sys.version}, {sys.copyright}")
        self.console_output.setFixedHeight(50)
        self.central_layout.addWidget(self.console_output)

        # Status bar
        self.status_bar = QtWidgets.QLabel("Статус бар", self.centralwidget)
        self.status_bar.setObjectName("status_bar")
        self.status_bar.setFixedHeight(25)
        self.central_layout.addWidget(self.status_bar)

        MainWindow.setCentralWidget(self.centralwidget)

        # Left dock widget
        self.left_dock = QtWidgets.QDockWidget("2 Меню", MainWindow)
        self.left_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.left_dock.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable |
                                   QtWidgets.QDockWidget.DockWidgetMovable |
                                   QtWidgets.QDockWidget.DockWidgetFloatable)
        self.left_dock.setWidget(QtWidgets.QWidget())
        MainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.left_dock)

        # Right dock widget
        self.right_dock = QtWidgets.QDockWidget("3 Меню", MainWindow)
        self.right_dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.right_dock.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable |
                                    QtWidgets.QDockWidget.DockWidgetMovable |
                                    QtWidgets.QDockWidget.DockWidgetFloatable)
        self.right_dock.setWidget(QtWidgets.QWidget())
        MainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.right_dock)

        # Connect button clicks to their functions
        self.project_button.clicked.connect(self.project_button_action)
        self.file_button.clicked.connect(self.file_button_action)

        # Set main window title
        MainWindow.setWindowTitle("Main Window")

    def project_button_action(self):
        self.console_output.append("Project button clicked")

    def file_button_action(self):
        self.console_output.append("File button clicked")
        self.setCentralWidget()

