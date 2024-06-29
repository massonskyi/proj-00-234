import os
from typing import List, Callable

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QMenuBar,
    QMainWindow
)

from gui.tools.subtools.custom_proxy_style import MyProxyStyle
from utils.loaders import load_icon


class CustomTitleBar(QWidget):
    def __init__(self, icons, callbacks, parent: QWidget | QMainWindow = None):
        super().__init__(parent)
        self.menubar = None
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
        self.style = MyProxyStyle('Fusion')
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
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        title_label = QPushButton(icon=self.icons.get("title_main"))
        title_label.setStyleSheet(
            """
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
        )
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
        minimize_button.setStyleSheet(
            """
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
        )
        layout.addWidget(minimize_button)

        # if isinstance(self.parent(), QMainWindow) and self.parent().objectName() == "MainWindow":
        self.maximize_button = QPushButton(icon=self.icons.get("maximize"))
        self.maximize_button.setFixedSize(55, 55)
        self.maximize_button.clicked.connect(self.toggle_maximized)
        self.maximize_button.setStyleSheet(
            """
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
        )
        layout.addWidget(self.maximize_button)

        close_button = QPushButton(icon=self.icons.get("close"))
        close_button.setFixedSize(55, 55)
        close_button.clicked.connect(self.__main_window.close)  # Close window
        close_button.setStyleSheet(
            """
                QPushButton {
                    background-color: transparent;
                    border: none;
                    font-size: 18px;
                    color: white;
                }
    
                QPushButton:hover {
                    background-color: rgba(212, 104, 104, 0.1);
                    color: red;
                }
            """
        )
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

        def create_action(text: str, icon: QtGui.QIcon, callback: Callable) -> QAction:
            action = QAction(text=text, icon=icon, parent=self)
            action.triggered.connect(callback)
            return action

        def add_actions(menu: QtWidgets.QMenu, actions: List[QAction]) -> None:
            for action in actions:
                menu.addAction(action)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setStyle(self.style)
        self.menubar.setStyleSheet(
            """
                QMenu {
                    background-color: #2e2e2e;
                    color: #ffffff;
                    border: 1px solid #1e1e1e;
                }
                QMenu::item {
                    color: #7097ba;
                }
                QMenu::item:selected {
                    background-color: #bfa7d4;
                    color: #000000;
                }
                QMenuBar::item {
                    color: #7097ba;
                }
                QMenuBar::item:selected {
                    background-color: #bfa7d4;
                    color: #000000;
                }
                QMenu::separator {
                    height: 1px;
                    background: #4e4e4e;
                    margin-left: 10px;
                    margin-right: 5px;
                }
            """
        )

        file_menu = self.menubar.addMenu("File")
        file_menu.setIcon(self.icons.get('menu_file'))

        # New menu
        new_menu = QtWidgets.QMenu("New", self)
        new_menu.setIcon(self.icons.get('menu_new'))
        new_file_action = create_action("New File", self.icons.get('menu_new_file'), self.callbacks['new_file'])
        new_project_action = create_action("New Project", self.icons.get('menu_new_project'),
                                           self.callbacks['new_project'])
        new_python_action = create_action("New Python File", self.icons.get('py'),
                                          self.callbacks.get('new_py_file', None)) if self.parent().pyconsole else None
        new_plain_text_action = create_action("New Plain Text", self.icons.get('menu_txt'),
                                              self.callbacks['new_txt_file'])
        add_actions(new_menu, [new_file_action, new_project_action])
        if new_python_action:
            new_menu.addAction(new_python_action)
        new_menu.addSeparator()
        new_menu.addAction(new_plain_text_action)

        # Open menu
        open_menu = QtWidgets.QMenu("Open", self)
        open_menu.setIcon(self.icons.get('menu_open'))
        open_file_action = create_action("Open File", self.icons.get('menu_file'), self.callbacks['open_file'])
        open_project_action = create_action("Open Project", self.icons.get('menu_open_project'),
                                            self.callbacks['open_project'])
        add_actions(open_menu, [open_file_action, open_project_action])

        # Save As menu
        save_menu = QtWidgets.QMenu("Save As", self)
        save_menu.setIcon(self.icons.get('menu_save_as'))
        save_actions = [
            create_action("docx", self.saves_icons['save_word'], self.callbacks['save']),
            create_action("xlsx", self.saves_icons['save_excel'], self.callbacks['save']),
            create_action("pdf", self.saves_icons['save_pdf'], self.callbacks['save']),
            create_action("csv", self.saves_icons['save_csv'], self.callbacks['save']),
            create_action("json", self.saves_icons['save_json'], self.callbacks['save']),
            create_action("html", self.saves_icons['save_html'], self.callbacks['save']),
            create_action("xml", self.saves_icons['save_xml'], self.callbacks['save']),
            create_action("txt", self.saves_icons['save_txt'], self.callbacks['save'])
        ]
        add_actions(save_menu, save_actions)

        # Add menus and actions to file_menu
        file_menu.addMenu(new_menu)
        file_menu.addMenu(open_menu)
        file_menu.addAction(create_action("Save", self.icons.get('menu_save'), self.callbacks['save_file']))
        file_menu.addMenu(save_menu)
        file_menu.addSeparator()
        file_menu.addAction(create_action("Exit", self.icons.get('menu_exit'), self.callbacks['close']))
        file_menu.setIcon(self.icons.get('main_menu'))

        # Projects menu
        projects_menu = self.menubar.addMenu(os.path.basename(self.parent().current_workspace))
        open_project_action = create_action("Open...", self.icons.get('menu_open'),
                                            self.callbacks['open_file_explorer'])
        projects_menu.addAction(open_project_action)
        projects_menu.addSeparator()

        current_project_action = create_action(os.path.basename(self.parent().current_workspace),
                                               self.icons.get('menu_open'),
                                               lambda: self.callbacks['save'](self.parent().current_workspace))
        projects_menu.addAction(current_project_action)

        current_project_path_action = QAction(text=self.parent().current_workspace, parent=self)
        current_project_path_action.setEnabled(False)
        projects_menu.addAction(current_project_path_action)
        projects_menu.addSeparator()

        return self.menubar
