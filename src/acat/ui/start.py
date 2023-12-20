from PyQt6.QtWidgets import QApplication

from acat.ui.main_window import MainWindow


def main() -> None:
    app = QApplication([])
    window = MainWindow()

    window.show()
    app.exec()
