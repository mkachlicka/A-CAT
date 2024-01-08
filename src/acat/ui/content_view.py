from collections import deque
from functools import partial
from typing import Callable, Deque, Iterable, List

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from acat.backend.judge_score import generate_praat_score
from acat.ui.audio_file import AudioFileInfo


class ContentTable(QTableWidget):
    COL_HEADERS = ["File Name", "Audio Length", "Score", "Actions"]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.data: Deque[AudioFileInfo] = deque()
        self._setup_list()

    def _setup_list(self) -> None:
        self.setColumnCount(len(self.COL_HEADERS))
        self.setHorizontalHeaderLabels(self.COL_HEADERS)
        self.setColumnWidth(3, 200)

    def add_row(self, row: AudioFileInfo) -> None:
        row_position = self.rowCount()

        self.insertRow(row_position)

        self.setItem(row_position, 0, QTableWidgetItem(row.file_name))
        self.setItem(row_position, 1, QTableWidgetItem(row.audio_length_str))
        self.setItem(row_position, 2, QTableWidgetItem(str(row.score)))

        self.setCellWidget(row_position, 3, self._create_actions(row_position))

        self.data.append(row)

    def _judge_row(self, row_position: int) -> None:
        try:
            row_data = self.data[row_position]
        except IndexError:
            QMessageBox.critical(
                self, "Error", "This is an internal error. Please notify the developer."
            )
            return

        if not row_data.path.exists():
            QMessageBox.critical(
                self,
                "Error",
                "This audio file does not exist. Please choose a proper file to analyze.",
            )
            return

        if row_data.path.is_dir():
            QMessageBox.critical(
                self,
                "Error",
                "A directory has been chosen, which shouldn't happen. Please notify the developer.",
            )
            return

        # TODO: implement text grid path
        generate_praat_score(row_data.path, row_data.text_grid_path)

    def _create_actions(self, row_position: int) -> QWidget:
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)

        judge_score_button = QPushButton("Judge")
        judge_score_button.clicked.connect(self._gen_judge_score_handle(row_position))

        open_file_info_button = QPushButton("Info")
        open_file_info_button.clicked.connect(self._gen_open_info_handle(row_position))

        button_layout.addWidget(judge_score_button)
        button_layout.addWidget(open_file_info_button)

        button_widget.setLayout(button_layout)

        return button_widget

    def add_rows(self, rows: Iterable[AudioFileInfo]) -> None:
        for row in rows:
            self.add_row(row)

    def _gen_open_info_handle(self, row_index: int) -> Callable:
        return partial(self.open_info, row_index)

    def _gen_judge_score_handle(self, row_index: int) -> Callable:
        return partial(self.judge_score, row_index)

    def open_info(self, row_index: int) -> None:
        # TODO: implement open info pop up
        pass

    def judge_score(self, row_index: int) -> None:
        if self._create_reanalyze_confirmation(self._check_if_analyzed(row_index)):
            self._judge_row(row_index)

    def judge_all_scores(self) -> None:
        if self._create_reanalyze_confirmation(self._check_if_analyzed()):
            for row_index in range(len(self.data)):
                self._judge_row(row_index)

    def _create_reanalyze_confirmation(self, files: List[str]) -> bool:
        if files:
            file_names = "\n".join(files)
            reply = QMessageBox.question(
                self,
                "Confirmation",
                f"The following files have already been analyzed:\n"
                f"{file_names}\n"
                f"Do you want to reanalyze them?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            return reply == QMessageBox.StandardButton.Yes
        else:
            return True

    def _check_if_analyzed(self, row_index: int | None = None) -> List[str]:
        if row_index is None:
            return list(
                map(
                    lambda row: row.file_name,
                    filter(lambda row: row.score is not None, self.data),
                )
            )

        try:
            row_to_check = self.data[row_index]
        except IndexError as e:
            QMessageBox.critical(
                self, "Error", "This is an internal error. Please notify the developer."
            )
            raise RuntimeError from e

        return [row_to_check.file_name] if row_to_check.score is not None else []


class ContentView(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.table = ContentTable()
        layout.addWidget(self.table)

        self.setLayout(layout)
