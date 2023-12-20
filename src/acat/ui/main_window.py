from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow

from acat.ui.content_view import ContentView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ACAT")
        self.resize(800, 600)

        self._create_actions()
        self._make_toolbar()
        self._make_content()

    def _check_if_dark_mode(self) -> bool:
        return self.palette().window().color().lightness() < 128

    def _create_actions(self) -> None:
        self._choose_action = QAction("&Choose", self)
        self._evaluate_all_action = QAction("&Evaluate All", self)
        self._export_action = QAction("&Export", self)

        self._help_action = QAction("&Help", self)
        self._load_sample_audio = QAction("&Load Sample", self)

    def _make_toolbar(self) -> None:
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
        # load sample audio action
        top_toolbar.addAction(self._load_sample_audio)

    def _make_content(self) -> None:
        self._content_view = ContentView()
        self.setCentralWidget(self._content_view)
