import pathlib

import pandas as pd
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QWidget, QWidgetAction

from acat.backend.judge_score import LanguageModel
from acat.ui.audio_file import AudioFileInfo, PraatScore
from acat.ui.content_view import ContentView
from acat.ui.help_window import HelpWindow
from acat.ui.ModelChooser import ModelComboChooser


class MainWindow(QMainWindow):
    """The main UI window of ACAT"""

    def __init__(self) -> None:
        super().__init__()

        self._help_window = None

        self.setWindowTitle("ACAT")
        self.resize(800, 600)

        self._create_actions()
        self._make_toolbar()
        self._make_content()

    def show(self) -> None:
        super().show()
        self._show_help_window()

    def _show_help_window(self) -> None:
        if self._help_window is None:
            self._help_window = HelpWindow()

        self.show_window(self._help_window)

    def show_window(self, widget: QWidget, bring_to_front: bool = True) -> None:
        main_window_geometry = self.frameGeometry()
        help_window_size = widget.sizeHint()
        center_point = main_window_geometry.center()
        widget.setGeometry(
            center_point.x() - help_window_size.width() // 2,
            center_point.y() - help_window_size.height() // 2,
            help_window_size.width(),
            help_window_size.height(),
        )
        widget.show()
        if bring_to_front:
            widget.activateWindow()

    def _check_if_dark_mode(self) -> bool:
        return self.palette().window().color().lightness() < 128

    def _create_actions(self) -> None:
        """Make the top toolbar of the application

        It creates toolbar button by using QAction
        and the actions are connected to its functionality by using the `.triggered.connect` function
        """
        self._choose_action = QAction("&Choose Audio", self)
        self._choose_action.triggered.connect(self._choose_file)

        self._evaluate_all_action = QAction("&Judge All", self)
        self._evaluate_all_action.triggered.connect(self._judge_all_rows)

        self._export_action = QAction("&Export", self)
        self._export_action.triggered.connect(self._export_to_csv)

        self._help_action = QAction("&Help", self)
        self._help_action.triggered.connect(self._show_help_window)

        self._model_box = ModelComboChooser()
        self._model_choose_action = QAction("&Choose Native Language", self)
        self._widget_action = QWidgetAction(self)
        self._widget_action.setDefaultWidget(self._model_box)

    def _export_results_as_df(self) -> pd.DataFrame:
        """Export data score as data frame"""
        data = []

        # dump scores into a 2d array
        for audio_file in self._content_view.table.data:
            file_name = audio_file.file_name
            file_path = str(audio_file.path)

            all_data = PraatScore.all_data_or_none(audio_file.score)

            data.append([file_name, file_path, *all_data])

        # make a dara frame for dumping
        df = pd.DataFrame(
            data,
            columns=[
                "File Name",
                "File Path",
                "Comprehensibility Score",
                "Nativelikeness Score",
                "speechrate",
                "pauses",
                "rangef0",
                "sdsylldur",
                "coeff1",
                "coeff2",
                "coeff3",
            ],
        )
        return df

    def _export_to_csv(self) -> None:
        """Dump the data into a CSV file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_path:
            df = self._export_results_as_df()
            df.to_csv(file_path, index=False)

    def _choose_file(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Audio Files",
            "",
            "Audio Files (*.wav *.mp3 *.py)",
        )

        file_info = [AudioFileInfo(pathlib.Path(file)) for file in files]

        self._content_view.table.add_rows(file_info)

    def _judge_all_rows(self) -> None:
        self._content_view.table.judge_all_scores(self.get_current_model())

    def get_current_model(self) -> LanguageModel:
        return LanguageModel(self._model_box.currentText())

    def _make_toolbar(self) -> None:
        """Add the made tool bar items into the top toolbar"""
        top_toolbar = self.addToolBar("General Actions")
        top_toolbar.setMovable(False)
        # choose file action
        top_toolbar.addAction(self._choose_action)
        top_toolbar.addSeparator()
        # evaluate all audio action
        top_toolbar.addAction(self._evaluate_all_action)
        top_toolbar.addSeparator()
        # file mode toggle
        # self._file_mode_toggle = FileModeToggle(parent=top_toolbar)
        # top_toolbar.addWidget(self._file_mode_toggle)
        # top_toolbar.addSeparator()
        # export results action
        top_toolbar.addAction(self._export_action)
        top_toolbar.addSeparator()
        # help action
        top_toolbar.addAction(self._help_action)
        top_toolbar.addSeparator()

        top_toolbar.addAction(self._model_choose_action)
        top_toolbar.addAction(self._widget_action)

    def _make_content(self) -> None:
        self._content_view = ContentView()
        self.setCentralWidget(self._content_view)
