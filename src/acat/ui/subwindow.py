from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget


class SubWindow(QWidget):
    def keyPressEvent(self, event):
        if (
            event.key() == Qt.Key.Key_W
            and event.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            self.close()
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
