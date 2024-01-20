from typing import Iterable, List, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QLayout,
    QTableWidget,
    QTableWidgetItem,
)

COMP_DATA = {
    "2.171 - 3.409": "Low comprehensibility – representing inexperienced L2 learners’ speech (no immersion experience)",
    "3.492 - 4.308": "Mid comprehensibility – representing moderately experienced L2 learners’ speech (LOR 1 month to 5 years)",
    "5.378 - 6.147": "High comprehensibility- representing long-term L2 residents’ speech (LOR 6-18 years)",
    "7.6": "Near-native L2 speaker (maximum)",
    "8.714 - 8.926": "Native speakers of English",
}

NAT_DATA = {
    "1.445 - 1.955": "Low nativelikeness – representing inexperienced L2 learners’ speech (no immersion experience)",
    "2.312 - 3.053": "Mid nativelikeness – representing moderately experienced L2 learners’ speech (LOR 1 month to 5 years)",
    "3.852 - 4.668": "High nativelikeness - representing long-term L2 residents’ speech (LOR 6-18 years)",
    "6.9": "Near-native L2 speaker (maximum)",
    "8.450 - 8.930": "Native speakers of English",
}


def make_rubrics(layout: QLayout) -> None:
    # Heading
    intro_text = QLabel("<h2>How to interpret</h2>")
    layout.addWidget(intro_text)

    # First Table: Comprehensibility Score
    comp_label = QLabel("<h3>comprehensibility score</h3>")
    layout.addWidget(comp_label)
    comp_headers = ["Comprehensibility Score", "Suggested interpretation"]
    _create_table(layout, comp_headers, COMP_DATA.items())

    # Second Table: Nativelikeness Score
    nat_label = QLabel("<h3>nativelikeness score</h3>")
    layout.addWidget(nat_label)
    nat_headers = ["Nativelikeness Score", "Suggested interpretation"]
    _create_table(layout, nat_headers, NAT_DATA.items())


def _create_table(
    layout: QLayout, headers: List[str], data: Iterable[Tuple[str, str]]
) -> None:
    table_style = (
        "QTableWidget {border: 1px solid black;}"
        "QTableWidget::item {border: 1px solid black;}"
    )
    table = QTableWidget()
    table.setRowCount(len(data))
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.horizontalHeader().setStretchLastSection(True)
    table.setStyleSheet(table_style)

    for row, (score, interpretation) in enumerate(data):
        score_item = QTableWidgetItem(score)
        score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        interpretation_item = QTableWidgetItem(interpretation)

        table.setItem(row, 0, score_item)
        table.setItem(row, 1, interpretation_item)

    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    layout.addWidget(table)
