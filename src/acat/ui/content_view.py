from __future__ import annotations

import traceback
import weakref
from typing import Callable, Iterable, List

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    Qt,
    QThreadPool,
    pyqtSignal,
    pyqtSlot,
)
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
from acat.ui.result_popup import ResultPopup
from acat.ui.window_management import get_main_window


class WorkerSignals(QObject):
    finished = pyqtSignal(int, object)


class RowWorker(QRunnable):
    def __init__(
        self, row_index: int, data: weakref.ReferenceType[AudioFileInfo]
    ) -> None:
        super().__init__()
        self.row_index = row_index
        self.data = data
        self.signal = WorkerSignals()

    @pyqtSlot()
    def run(self):
        data: AudioFileInfo = self.data()
        if data is None:
            return

        try:
            data.score = generate_praat_score(data.path)
        except Exception as e:
            print(
                "Error",
                "An error occurred while analyzing the audio file. Please notify the developer.",
            )
            raise RuntimeError from e

        self.signal.finished.emit(self.row_index, data)


class ContentTable(QTableWidget):
    COL_HEADERS = ["File Name", "Audio Length", "Comp Score", "Nat Score", "Actions"]
    ACTION_COL = 4

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.data: List[AudioFileInfo] = []
        self._setup_list()
        self._thread_pool = QThreadPool()
        self._threads = []
        self._selected: weakref.ReferenceType[AudioFileInfo] | None = None

    def _setup_list(self) -> None:
        self.setColumnCount(len(self.COL_HEADERS))
        self.setHorizontalHeaderLabels(self.COL_HEADERS)
        self.setColumnWidth(self.ACTION_COL, 200)

        self.popup = ResultPopup()

    def add_row(self, row: AudioFileInfo) -> None:
        row_position = self.rowCount()

        self.insertRow(row_position)

        file_name_item = QTableWidgetItem(row.file_name)
        file_name_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setItem(row_position, 0, file_name_item)

        audio_length_item = QTableWidgetItem(row.audio_length_str)
        audio_length_item.setTextAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        self.setItem(row_position, 1, audio_length_item)

        score_item = QTableWidgetItem(row.comprehensibility_str)
        score_item.setTextAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        self.setItem(row_position, 2, score_item)

        score_item = QTableWidgetItem(row.nativelikeness_str)
        score_item.setTextAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        self.setItem(row_position, 3, score_item)

        self.setCellWidget(row_position, 4, self._create_actions())

        self.data.append(row)

    def _judge_row(self, row_position: int) -> None:
        row_data = self.get_row(row_position, notify=True)

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

        thread = RowWorker(row_position, weakref.ref(row_data))
        thread.signal.finished.connect(self._update_score)
        self._thread_pool.start(thread)

    def _update_score(self, row_index: int, data: AudioFileInfo) -> None:
        row_data = self.get_row(row_index)
        if row_data is data:
            self.setItem(
                row_index,
                2,
                QTableWidgetItem(row_data.comprehensibility_str),
            )
            self.setItem(row_index, 3, QTableWidgetItem(row_data.nativelikeness_str))

            if self._selected and self._selected() == data:
                self.popup.update_content(row_data)

    def _create_actions(self) -> QWidget:
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)

        judge_score_button = QPushButton("Judge")
        judge_score_button.clicked.connect(
            self._gen_handle("judge_score", weakref.ref(button_widget))
        )

        open_file_info_button = QPushButton("Info")
        open_file_info_button.clicked.connect(
            self._gen_handle("open_info", weakref.ref(button_widget))
        )

        del_row_button = QPushButton("Delete")
        del_row_button.clicked.connect(
            self._gen_handle("delete_row", weakref.ref(button_widget))
        )

        button_layout.addWidget(judge_score_button)
        button_layout.addWidget(open_file_info_button)
        button_layout.addWidget(del_row_button)

        button_widget.setLayout(button_layout)

        return button_widget

    def add_rows(self, rows: Iterable[AudioFileInfo]) -> None:
        for row in rows:
            self.add_row(row)

    def _gen_handle(
        self, handle_name: str, action_widget: weakref.ReferenceType[QWidget]
    ) -> Callable:
        def _inner() -> None:
            row_index = self._find_row_index(action_widget())
            getattr(self, handle_name)(row_index)

        return _inner

    def _find_row_index(self, widget: QWidget | None) -> int:
        if widget is None:
            return -1

        for row_index in range(self.rowCount()):
            if self.cellWidget(row_index, self.ACTION_COL) is widget:
                return row_index

    def delete_row(self, row_index: int) -> None:
        self.removeRow(row_index)
        self.data.pop(row_index)

    def open_info(self, row_index: int) -> None:
        data = self.get_row(row_index)
        self._selected = weakref.ref(data)

        get_main_window().show_window(self.popup.update_content(data))

    def get_row(self, row_index: int, notify: bool = False) -> AudioFileInfo | None:
        try:
            return self.data[row_index]
        except IndexError as e:
            if notify:
                QMessageBox.critical(
                    self,
                    "Error",
                    "This is an internal error. Please notify the developer.\n"
                    f"{traceback.format_tb(e.__traceback__)}",
                )
        return None

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

        row_to_check = self.get_row(row_index, notify=True)

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
