from PySide6.QtCore import QEvent
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow


class CustomGraphWidget:
    pass


class GraphWindow(QMainWindow):
    """
    Wrapper class for the graph window.
    """
    def __init__(self, graph_widget: CustomGraphWidget, parent=None) -> None:
        """
        Initialise the graph window. This is called when the window is created.
        :param graph_widget: The graph widget.
        :param parent: The parent widget for the window.
        """
        super().__init__(parent)
        self.graph_widget = graph_widget
        self.setWindowTitle("Graph")
        self.setCentralWidget(self.graph_widget)
        self.resize(600, 300)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Close the window when the window is closed. This is called when the window is closed.
        :param event: QCloseEvent
        :return: None
        """
        self.graph_widget.setParent(None)
        self.parent()._add_graph()
