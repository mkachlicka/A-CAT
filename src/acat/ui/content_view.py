from functools import partial
from typing import Callable, Tuple

from PyQt6.QtWidgets import (
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

RowInfoType = Tuple[str, int, float | None]


class ContentTable(QTableWidget):
    COL_HEADERS = ["File Name", "Audio Length", "Score", "Judge", "Open"]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_list()

    def _setup_list(self) -> None:
        self.setColumnCount(len(self.COL_HEADERS))
        self.setHorizontalHeaderLabels(self.COL_HEADERS)

    def add_row(self, row: RowInfoType) -> None:
        row_position = self.rowCount()

        self.insertRow(row_position)

        file_name, audio_length, score = row

        self.setItem(row_position, 0, QTableWidgetItem(file_name))
        self.setItem(row_position, 1, QTableWidgetItem(str(audio_length)))
        self.setItem(row_position, 2, QTableWidgetItem(str(score)))

        judge_score_button = QPushButton("Judge Score")
        judge_score_button.clicked.connect(self._gen_judge_score_handle(row_position))
        self.setCellWidget(row_position, 3, judge_score_button)

        open_file_info_button = QPushButton("Open File Info")
        open_file_info_button.clicked.connect(self._gen_open_info_handle(row_position))
        self.setCellWidget(row_position, 4, open_file_info_button)

    def _gen_open_info_handle(self, row_index: int) -> Callable:
        return partial(self.open_info, row_index)

    def _gen_judge_score_handle(self, row_index: int) -> Callable:
        return partial(self.judge_score, row_index)

    def open_info(self, row_index: int) -> None:
        # TODO: implement open info pop up
        pass

    def judge_score(self, row_index: int) -> None:
        # TODO: implement judge score handle
        pass


class ContentView(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.table = ContentTable()
        layout.addWidget(self.table)

        self.setLayout(layout)
