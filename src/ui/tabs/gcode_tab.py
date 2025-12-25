"""G-code control tab."""

from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt

from ..widgets.gcode_editor import GCodeEditor


def _editor_group() -> QGroupBox:
    group = QGroupBox("Editor")
    layout = QVBoxLayout()

    info = QLabel("Line numbers | Syntax highlight | Search & replace")
    layout.addWidget(info)

    search_row = QHBoxLayout()
    search = QLineEdit()
    search.setPlaceholderText("Search in G-code...")
    search_row.addWidget(search)
    search_row.addWidget(QPushButton("Find Next"))
    layout.addLayout(search_row)

    layout.addWidget(GCodeEditor())

    button_row = QHBoxLayout()
    button_row.addWidget(QPushButton("Load File"))
    button_row.addWidget(QPushButton("Save"))
    button_row.addWidget(QPushButton("Validate"))
    layout.addLayout(button_row)

    group.setLayout(layout)
    return group


def _simulation_group() -> QGroupBox:
    group = QGroupBox("Simulation Control")
    layout = QVBoxLayout()

    speed_row = QHBoxLayout()
    speed_row.addWidget(QLabel("Speed: 1.0x"))
    speed_slider = QSlider(Qt.Horizontal)
    speed_slider.setMinimum(1)
    speed_slider.setMaximum(200)
    speed_row.addWidget(speed_slider)
    layout.addLayout(speed_row)

    button_row = QHBoxLayout()
    button_row.addWidget(QPushButton("Start"))
    button_row.addWidget(QPushButton("Pause"))
    button_row.addWidget(QPushButton("Stop"))
    layout.addLayout(button_row)

    progress_row = QHBoxLayout()
    progress_row.addWidget(QLabel("Current line: 120/450"))
    progress_slider = QSlider(Qt.Horizontal)
    progress_slider.setMinimum(0)
    progress_slider.setMaximum(450)
    progress_row.addWidget(progress_slider)
    layout.addLayout(progress_row)

    step_row = QHBoxLayout()
    step_row.addWidget(QPushButton("Step +"))
    step_row.addWidget(QPushButton("Step -"))
    step_row.addWidget(QPushButton("Step Forward"))
    step_row.addWidget(QPushButton("Step Back"))
    layout.addLayout(step_row)

    group.setLayout(layout)
    return group


class GCodeTab(QWidget):
    """Tab for G-code control."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(_editor_group())
        layout.addWidget(_simulation_group())
        layout.addStretch()
        self.setLayout(layout)
