"""G-code editor widget."""

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPlainTextEdit


class GCodeEditor(QPlainTextEdit):
    """Plain text editor with sample G-code."""

    def __init__(self) -> None:
        super().__init__()
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setFont(QFont("Courier New", 10))
        self.setPlainText(
            "N10 G90 G94\n"
            "N20 M03 S10000\n"
            "N30 G01 X0 Y0 Z5 F1500\n"
            "N40 G01 X50 Y0 Z-2\n"
            "N50 G01 X50 Y50 Z-2\n"
        )
