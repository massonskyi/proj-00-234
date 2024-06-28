import os

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QListWidget, QVBoxLayout, QMenuBar, \
    QMainWindow, QMenu, QProxyStyle, QStyle

from utils.loaders import load_icon


class MyProxyStyle(QProxyStyle):
    pass

    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

        if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
            return 55
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


class CustomTitleBar(QWidget):
    def __init__(self, icons, callbacks, parent: QWidget | QMainWindow = None):
        super().__init__(parent)
        self.__main_window = parent
        self.maximize_button = None
        self.file_path_label = None
        self.callbacks = callbacks
        self.setMouseTracking(True)
        self.current_workspace = self.parent().current_workspace
        self.current_open_file = self.parent().current_open_file
        self._startPos = None
        self._clickPos = None
        self._dragPos = None
        self.icons = icons
        self.style = MyProxyStyle('Fusion')    # The proxy style should be based on an existing style,
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

        self.setup_ui()

    def hide_file_path_label(self):
        if self.parent().width() > 600:
            self.file_path_label.show()
        else:
            self.file_path_label.hide()

    def setup_ui(self):
        button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 18px;
                color: white;
            }

            QPushButton:hover {
                background-color: rgba(182, 145, 214, 0.1);
                color: red;
            }
        """

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        title_label = QPushButton(icon=self.icons.get("title_main"))
        title_label.setStyleSheet(button_style)
        title_label.setFixedSize(55, 55)
        layout.addWidget(title_label)

        # if isinstance(self.parent(), QMainWindow) and self.parent().objectName() == "MainWindow":
        menu_widget = self.setupUiMenu()
        menu_widget.setFixedWidth(150)

        layout.addWidget(menu_widget)
        layout.addStretch()
        if self.__main_window.width() > 550:
            self.file_path_label = QLabel(
                f"{os.path.basename(self.__main_window.current_open_file)} [{self.__main_window.current_workspace}]")
            self.file_path_label.setObjectName("file_path_label")
            self.file_path_label.setStyleSheet("color: #7097ba")
            self.file_path_label.setFixedWidth(
                QLabel(
                    f"{os.path.basename(self.__main_window.current_open_file)} [{self.__main_window.current_workspace}]").width())
            self.file_path_label.setAlignment(Qt.AlignCenter)

            layout.addWidget(self.file_path_label)
        layout.addStretch()

        minimize_button = QPushButton(icon=self.icons.get("minimize"))
        minimize_button.setFixedSize(55, 55)
        minimize_button.clicked.connect(self.__main_window.showMinimized)
        minimize_button.setStyleSheet(button_style)
        layout.addWidget(minimize_button)

        # if isinstance(self.parent(), QMainWindow) and self.parent().objectName() == "MainWindow":
        self.maximize_button = QPushButton(icon=self.icons.get("maximize"))
        self.maximize_button.setFixedSize(55, 55)
        self.maximize_button.clicked.connect(self.toggle_maximized)
        self.maximize_button.setStyleSheet(button_style)
        layout.addWidget(self.maximize_button)

        close_button = QPushButton(icon=self.icons.get("close"))
        close_button.setFixedSize(55, 55)
        close_button.clicked.connect(self.__main_window.close)  # Close window
        close_button.setStyleSheet(button_style)
        layout.addWidget(close_button)
        self.setLayout(layout)

    def update_current_open_file(self, filepath):
        self.current_open_file = filepath
        self.file_path_label.setText(f"{os.path.basename(self.__main_window.current_open_file)} [{self.__main_window.current_workspace}]")
        self.file_path_label.setFixedWidth(
            QLabel(f"{os.path.basename(self.__main_window.current_open_file)} [{self.__main_window.current_workspace}]").width())

    def update_current_workspace(self, workspace):
        self.current_workspace = workspace
        self.file_path_label.setText(f"{os.path.basename(self.__main_window.current_open_file)} [{self.__main_window.current_workspace}]")
        self.file_path_label.setFixedWidth(
            QLabel(f"{os.path.basename(self.__main_window.current_open_file)} [{self.__main_window.current_workspace}]").width())

    def toggle_maximized(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._startPos = self.mapToGlobal(event.pos())
            self._clickPos = self.mapToParent(event.pos())
            self._dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self._dragPos = event.globalPos()
            self.parent().move(self._dragPos - self._clickPos)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_maximized()

    def setupUiMenu(self) -> QtWidgets.QMenuBar:
        """
        Setup the main window menu
        :return: QtWidgets.QMenuBar
        """

        def configure_menu(menubar: QtWidgets.QMenuBar) -> None:
            new_menu = QtWidgets.QMenu("New", self)
            new_menu.setIcon(self.icons.get('menu_new'))
            new_file_action = QAction(text="New File", icon=self.icons.get('menu_new_file'), parent=self)
            new_file_action.triggered.connect(self.callbacks['new_file'])
            new_project_action = QAction(text="New Project", icon=self.icons.get('menu_new_project'), parent=self)
            new_project_action.triggered.connect(self.callbacks['new_project'])

            if self.parent().pyconsole:
                new_python_action = QAction(text="New Python File", icon=self.icons.get('py'), parent=self)
                new_python_action.triggered.connect(self.callbacks['new_py_file'])

            new_plain_text_action = QAction(text="New Plain Text", icon=self.icons.get('menu_txt'), parent=self)
            new_plain_text_action.triggered.connect(self.callbacks['new_txt_file'])
            new_menu.addAction(new_file_action)
            new_menu.addAction(new_project_action)
            new_menu.addSeparator()

            if self.parent().pyconsole:
                new_menu.addAction(new_python_action)

            new_menu.addAction(new_plain_text_action)

            # Open submenu
            open_menu = QtWidgets.QMenu("Open", self)
            open_menu.setIcon(self.icons.get('menu_open'))
            open_file_action = QAction(text="Open File", icon=self.icons.get('menu_file'), parent=self)
            open_file_action.triggered.connect(self.callbacks['open_file'])
            open_project_action = QAction(text="Open Project", icon=self.icons.get('menu_open_project'), parent=self)
            open_project_action.triggered.connect(self.callbacks['open_project'])
            open_menu.addAction(open_file_action)
            open_menu.addAction(open_project_action)

            save_menu = QtWidgets.QMenu("Save As", self)
            save_menu.setIcon(self.icons.get('menu_save_as'))
            save_to_word_action = QAction(text="docx", icon=self.saves_icons['save_word'], parent=self)
            save_to_word_action.setObjectName("save_to_word")
            save_to_word_action.triggered.connect(self.callbacks['save'])

            save_to_excel_action = QAction(text="xlsx", icon=self.saves_icons['save_excel'], parent=self)
            save_to_excel_action.setObjectName("save_to_excel")
            save_to_excel_action.triggered.connect(self.callbacks['save'])

            save_to_pdf_action = QAction(text="pdf", icon=self.saves_icons['save_pdf'], parent=self)
            save_to_pdf_action.setObjectName("save_to_pdf")
            save_to_pdf_action.triggered.connect(self.callbacks['save'])

            save_to_csv_action = QAction(text="csv", icon=self.saves_icons['save_csv'], parent=self)
            save_to_csv_action.setObjectName("save_to_csv")
            save_to_csv_action.triggered.connect(self.callbacks['save'])

            save_to_json_action = QAction(text="json", icon=self.saves_icons['save_json'], parent=self)
            save_to_json_action.setObjectName("save_to_json")
            save_to_json_action.triggered.connect(self.callbacks['save'])

            save_to_html_action = QAction(text="html", icon=self.saves_icons['save_html'], parent=self)
            save_to_html_action.setObjectName("save_to_html")
            save_to_html_action.triggered.connect(self.callbacks['save'])

            save_to_xml_action = QAction(text="xml", icon=self.saves_icons['save_xml'], parent=self)
            save_to_xml_action.setObjectName("save_to_xml")
            save_to_xml_action.triggered.connect(self.callbacks['save'])

            save_to_txt_action = QAction(text="txt", icon=self.saves_icons['save_txt'], parent=self)
            save_to_txt_action.setObjectName("save_to_txt")
            save_to_txt_action.triggered.connect(self.callbacks['save'])

            save_menu.addAction(save_to_word_action)
            save_menu.addAction(save_to_excel_action)
            save_menu.addAction(save_to_pdf_action)
            save_menu.addAction(save_to_csv_action)
            save_menu.addAction(save_to_json_action)
            save_menu.addAction(save_to_html_action)
            save_menu.addAction(save_to_xml_action)
            save_menu.addAction(save_to_txt_action)

            file_menu = menubar.addMenu("File")

            file_menu.setIcon(self.icons.get('menu_file'))
            file_menu.addMenu(new_menu)
            file_menu.addMenu(open_menu)
            save_action = QAction(text="Save", icon=self.icons.get('menu_save'), parent=self)
            save_action.triggered.connect(self.callbacks['save_file'])
            file_menu.addAction(save_action)

            file_menu.addMenu(save_menu)
            file_menu.addSeparator()
            exit_action = QAction(text="Exit", icon=self.icons.get('menu_exit'), parent=self)
            exit_action.triggered.connect(self.callbacks['close'])
            file_menu.addAction(exit_action)
            file_menu.setIcon(self.icons.get('main_menu'))

            projects_menu = menubar.addMenu(os.path.basename(self.parent().current_workspace))
            open_project_action = QAction(text="Open...", icon=self.icons.get('menu_open'), parent=self)
            open_project_action.triggered.connect(self.callbacks['open_file_explorer'])
            projects_menu.addAction(open_project_action)

            projects_menu.addSeparator()

            current_project_action = QAction(text=os.path.basename(self.parent().current_workspace),
                                             icon=self.icons.get('menu_open'), parent=self)
            current_project_action.triggered.connect(
                lambda: self.callbacks['save'](self.parent().current_workspace))
            projects_menu.addAction(current_project_action)

            current_project_path_action = QAction(text=self.parent().current_workspace, parent=self)
            current_project_path_action.setEnabled(False)
            projects_menu.addAction(current_project_path_action)

            projects_menu.addSeparator()

        self.menubar = QMenuBar(self)
        self.menubar.setStyle(self.style)
        self.menubar.setStyleSheet("""
                QMenu {
                    background-color: #2e2e2e;
                    color: #ffffff;
                    border: 1px solid #1e1e1e;
                }
                QMenu::item {
                    color: #7097ba;
                }
                QMenu::separator {
                    height: 1px;
                    background: #4e4e4e;
                    margin-left: 10px;
                    margin-right: 5px;
                }
            """)
        configure_menu(self.menubar)
        return self.menubar
