from PyQt6.QtWidgets import QApplication

from acat.ui.main_window import MainWindow
from acat.ui.window_management import get_main_window, set_main_window


def start_application() -> None:
    app = QApplication([])

    set_main_window(MainWindow())
    get_main_window().show()

    app.exec()
