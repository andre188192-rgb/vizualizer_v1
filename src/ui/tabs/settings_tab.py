"""Settings tab."""

from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


def _graphics_group() -> QGroupBox:
    group = QGroupBox("Graphics")
    form = QFormLayout()
    quality = QComboBox()
    quality.addItems(["Low", "Medium", "High", "Ultra"])
    form.addRow("Quality", quality)

    aa = QComboBox()
    aa.addItems(["Off", "2x", "4x", "8x"])
    form.addRow("Anti-aliasing", aa)

    fps_limit = QSpinBox()
    fps_limit.setRange(15, 240)
    fps_limit.setValue(60)
    form.addRow("FPS limit", fps_limit)

    show_fps = QCheckBox()
    show_fps.setChecked(True)
    form.addRow("Show FPS", show_fps)
    group.setLayout(form)
    return group


def _controls_group() -> QGroupBox:
    group = QGroupBox("Controls")
    form = QFormLayout()
    form.addRow("Invert X", QCheckBox())
    form.addRow("Invert Y", QCheckBox())
    form.addRow("Invert Z", QCheckBox())

    mouse_sense = QDoubleSpinBox()
    mouse_sense.setRange(0.1, 5.0)
    mouse_sense.setValue(1.0)
    form.addRow("Mouse sensitivity", mouse_sense)

    wheel_sense = QDoubleSpinBox()
    wheel_sense.setRange(0.1, 5.0)
    wheel_sense.setValue(1.0)
    form.addRow("Wheel sensitivity", wheel_sense)
    group.setLayout(form)
    return group


def _system_group() -> QGroupBox:
    group = QGroupBox("System")
    form = QFormLayout()
    autosave = QCheckBox()
    autosave.setChecked(True)
    form.addRow("Autosave", autosave)

    language = QComboBox()
    language.addItems(["Русский", "English"])
    form.addRow("Language", language)

    theme = QComboBox()
    theme.addItems(["Dark", "Light"])
    form.addRow("Theme", theme)

    group.setLayout(form)
    return group


class SettingsTab(QWidget):
    """Tab for application settings."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(_graphics_group())
        layout.addWidget(_controls_group())
        layout.addWidget(_system_group())
        layout.addStretch()
        self.setLayout(layout)
