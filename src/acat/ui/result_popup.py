from typing import Self

from PyQt6.QtWidgets import QLabel, QVBoxLayout

from acat.ui.audio_file import AudioFileInfo
from acat.ui.rubrics import make_rubrics
from acat.ui.subwindow import SubWindow


class ResultPopup(SubWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.title_label = QLabel("Score Details")
        self.comprehensibility_label = QLabel("Comprehensibility")
        self.nativelikeness_label = QLabel("Nativelikeness")

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.comprehensibility_label)
        self.layout.addWidget(self.nativelikeness_label)

        make_rubrics(self.layout)

    def update_content(self, audio_info: AudioFileInfo) -> Self:
        self.title_label.setText(f'<h1>The score of "{audio_info.file_name}"</h1>')
        self.comprehensibility_label.setText(
            f"<p>Comprehensibility: <bold>{audio_info.comprehensibility_str}</bold></p>"
        )
        self.nativelikeness_label.setText(
            f"<p>Nativelikeness: <bold>{audio_info.nativelikeness_str}</bold></p>"
        )

        self.setWindowTitle(f"Audio Details Of {audio_info.file_name}")

        return self
