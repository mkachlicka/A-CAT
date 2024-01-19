from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget


class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Help Window")

        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setPlainText("Help Message 1\nHelp Message 2\nHelp Message 3")
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        self.setLayout(layout)
