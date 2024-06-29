import sys
import time
from PySide6.QtCore import Qt, QThread, Signal, QEventLoop
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QProgressBar, QPushButton
from time import perf_counter


class LoaderThread(QThread):
    """
    LoaderThread is a thread that runs a function in a separate thread
    """
    progress_update = Signal(int)  # Сигнал для обновления прогресса
    task_completed = Signal()  # Сигнал для завершения задачи

    def __init__(self, function_to_run: callable, *args, **kwargs) -> None:
        """
        Initializes the thread with the given function to run
        """
        super().__init__(*args, **kwargs)
        self.task = function_to_run
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        """
        Runs the function in the separate thread and updates the progress bar
        :return: None
        """

        elapsed_time = self._calculate_emulate_time_running()

        for i in range(101):
            QThread.msleep(int(elapsed_time * 10))  # Задержка пропорционально времени выполнения
            self._update_progress(i)  # Отправка сигнала с обновлением прогресса
        print([next(iter) for iter in self.task(*self.args, **self.kwargs)])
        self.task_completed.emit()

    def _update_progress(self, progress: int) -> None:
        """
        Updates the progress bar with the given progress value
        :param progress: the progress value
        :return: None
        """
        self.progress_update.emit(progress)

    def _calculate_emulate_time_running(self) -> float:
        """
        Calculates the elapsed time of the function in seconds. Returns the elapsed time in seconds
        :return: elapsed time in seconds in seconds
        """
        start_time = perf_counter()
        self.task(*self.args, **self.kwargs)
        end_time = perf_counter()
        elapsed_time = end_time - start_time
        return elapsed_time
