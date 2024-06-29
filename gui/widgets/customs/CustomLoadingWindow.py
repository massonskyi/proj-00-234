from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar


class LoadingWindow(QWidget):
    """
    LoadingWindow class
    """

    def __init__(self, parent=None) -> None:
        """
        Initializes the LoadingWindow class
        :param callbacks: List[Callable]
        """
        super().__init__(parent)
        self.thread = None
        self.setWindowTitle("Loading")
        self.setGeometry(300, 300, 300, 100)
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QLabel {
                font-size: 16px;
                padding: 10px;
            }
            QProgressBar {
                border: 2px solid #FFFFFF;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
                margin: 1px;
            }
        """)

        self.layout = QVBoxLayout()

        self.label = QLabel("Loading data...")
        self.layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

    def update_progress(self, value: int) -> None:
        """
        Updates the progress bar value
        :param value: The value to update the progress bar value
        """
        self.label.setText(f"Processing data... {value}%")
        self.progress_bar.setValue(value)

    def display_time(self, elapsed_time: float) -> None:
        """
        Displays the time elapsed since the start of the loading process
        :param elapsed_time: The time elapsed since the start of the loading process
        """
        self.label.setText(f"Loading completed in {elapsed_time:.2f} seconds")
        self.progress_bar.setValue(100)
