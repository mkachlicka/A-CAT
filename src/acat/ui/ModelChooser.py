from PyQt6.QtWidgets import QComboBox

from acat.backend.judge_score import LanguageModel


class ModelComboChooser(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addItems([model.name for model in LanguageModel])
