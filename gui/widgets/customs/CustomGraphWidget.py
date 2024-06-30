import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget


class CustomGraphWidget(QWidget):
    """
    Custom Graph Widget for PySide6
    """

    def __init__(self, parent=None) -> None:
        """
        Custom Graph Widget for PySide6
        """
        super().__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        """
        Initialize the UI
        """
        layout = QVBoxLayout(self)
        self.plotWidget = pg.PlotWidget()
        layout.addWidget(self.plotWidget)

    def plot(self, data: list) -> None:
        """
        Plot the data
        """
        self.plotWidget.clear()
        x = [i for i in range(len(data))]
        y = [int(item) for item in data]

        self.plotWidget.plot(x, y, symbol='o', symbolSize=3, pen=pg.mkPen(color=(255, 0, 0), width=2))

    def plot_histogram(self, data: list) -> None:
        """
        Plot the data as a bar graph
        """
        self.plotWidget.clear()
        x = [i for i in range(len(data))]
        y = [int(item) for item in data]

        # Create a bar graph item
        bg1 = pg.BarGraphItem(x=x, height=y, width=0.6, brush='r')
        self.plotWidget.addItem(bg1)

    def clear(self) -> None:
        """
        Clear the plot
        """
        self.plotWidget.clear()
        self.plotWidget.plotItem.clear()
