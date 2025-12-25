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


def _editor_group() -> tuple[
    QGroupBox,
    QLineEdit,
    QPushButton,
    QPushButton,
    QPushButton,
    GCodeEditor,
]:
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

    editor = GCodeEditor()
    layout.addWidget(editor)

    button_row = QHBoxLayout()
    load_button = QPushButton("Load File")
    save_button = QPushButton("Save")
    validate_button = QPushButton("Validate")
    button_row.addWidget(load_button)
    button_row.addWidget(save_button)
    button_row.addWidget(validate_button)
    layout.addLayout(button_row)

    group.setLayout(layout)
    return group, search, load_button, save_button, validate_button, editor


def _simulation_group() -> tuple[
    QGroupBox,
    QSlider,
    QPushButton,
    QPushButton,
    QPushButton,
    QSlider,
]:
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
    start_button = QPushButton("Start")
    pause_button = QPushButton("Pause")
    stop_button = QPushButton("Stop")
    button_row.addWidget(start_button)
    button_row.addWidget(pause_button)
    button_row.addWidget(stop_button)
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
    return group, speed_slider, start_button, pause_button, stop_button, progress_slider
    return group


class GCodeTab(QWidget):
    """Tab for G-code control."""

    def __init__(self) -> None:
        super().__init__()
        (
            self.editor_group,
            self.search_input,
            self.load_button,
            self.save_button,
            self.validate_button,
            self.editor,
        ) = _editor_group()
        (
            self.simulation_group,
            self.speed_slider,
            self.start_button,
            self.pause_button,
            self.stop_button,
            self.progress_slider,
        ) = _simulation_group()

        layout = QVBoxLayout()
        layout.addWidget(self.editor_group)
        layout.addWidget(self.simulation_group)
        layout.addStretch()
        self.setLayout(layout)

    def gcode_text(self) -> str:
        return self.editor.toPlainText()

    def set_gcode_text(self, text: str) -> None:
        self.editor.setPlainText(text)

    def set_progress(self, current: int, total: int) -> None:
        self.progress_slider.setMaximum(max(total, 1))
        self.progress_slider.setValue(current)
        layout = QVBoxLayout()
        layout.addWidget(_editor_group())
        layout.addWidget(_simulation_group())
        layout.addStretch()
        self.setLayout(layout)
