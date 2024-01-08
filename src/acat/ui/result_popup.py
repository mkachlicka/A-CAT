from typing import Self

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from acat.ui.audio_file import AudioFileInfo


class ResultPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.title_label = QLabel("Score Details")
        self.comprehensibility_label = QLabel("Comprehensibility")
        self.nativelikeness_label = QLabel("Nativelikeness")

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.comprehensibility_label)
        self.layout.addWidget(self.nativelikeness_label)

    def update_content(self, audio_info: AudioFileInfo) -> Self:
        self.title_label.setText(f'The score of "{audio_info.file_name}"')
        self.comprehensibility_label.setText(
            f"Comprehensibility: {audio_info.comprehensibility_str}"
        )
        self.nativelikeness_label.setText(
            f"Nativelikeness: {audio_info.nativelikeness_str}"
        )

        self.setWindowTitle(f"Audio Details Of {audio_info.file_name}")

        return self
