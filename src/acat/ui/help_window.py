from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from acat.ui.rubrics import make_rubrics


class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Help Window")

        layout = QVBoxLayout()
        # Heading
        heading = QLabel("<h1>Automated Comprehensibility Assessment Tool</h1>")
        layout.addWidget(heading)

        # Bullet Points
        instruction = QLabel("<h2>Usage Instructions</h2>")
        layout.addWidget(instruction)
        bullet_points = QLabel(
            """
                    <ul>
                        <li>Choose one or multiple ".wav" audio files using the choose button on the top left; if you don't have the files right now and wants to try this app, you can click the "Load Sample" button.</li>
                        <li>Click "Judge All" to evaluate all chosen files, or click the "Judge" button for each individual file.</li>
                        <li>Check out the judged scores in the table below and you can click the "Info" button for each file to see detailed explanations.</li>
                        <li>You can export the results as a CSV file using the "Export" Button.</li>
                    </ul>
                """
        )
        bullet_points.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(bullet_points)

        # Hyperlink Paragraph
        hyperlink_paragraph = QLabel(
            'For more information, please visit <a href="https://link.here">the application website</a>.'
        )
        hyperlink_paragraph.setOpenExternalLinks(True)
        layout.addWidget(hyperlink_paragraph)

        # Rubrics
        make_rubrics(layout)

        self.setLayout(layout)
