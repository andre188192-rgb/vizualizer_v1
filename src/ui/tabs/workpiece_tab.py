"""Workpiece setup tab."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


def _dimensions_group() -> QGroupBox:
    group = QGroupBox("Dimensions & Material")
    form = QFormLayout()
    for label, value in (("Width", 200.0), ("Height", 100.0), ("Depth", 50.0)):
        spin = QDoubleSpinBox()
        spin.setRange(1.0, 2000.0)
        spin.setValue(value)
        spin.setSuffix(" mm")
        form.addRow(label, spin)

    material = QComboBox()
    material.addItems(["Aluminum", "Steel", "Wood", "Plastic"])
    form.addRow("Material", material)

    color_button = QPushButton("Choose color")
    form.addRow("Color", color_button)

    zero_point = QComboBox()
    zero_point.addItems(["Top Center", "Top Left", "Bottom Center"])
    form.addRow("Zero Point", zero_point)
    group.setLayout(form)
    return group


def _position_group() -> QGroupBox:
    group = QGroupBox("Position")
    layout = QVBoxLayout()

    for axis in ("X", "Y", "Z"):
        row = QHBoxLayout()
        row.addWidget(QLabel(f"{axis}:"))
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(-50)
        slider.setMaximum(50 if axis != "Z" else 100)
        row.addWidget(slider)
        row.addWidget(QLabel("0"))
        layout.addLayout(row)

    group.setLayout(layout)
    return group


def _import_group() -> QGroupBox:
    group = QGroupBox("Import / Export")
    layout = QHBoxLayout()
    layout.addWidget(QPushButton("Import STL"))
    layout.addWidget(QPushButton("Export as STL"))
    layout.addWidget(QPushButton("Reset Workpiece"))
    group.setLayout(layout)
    return group


class WorkpieceTab(QWidget):
    """Tab for workpiece setup."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(_dimensions_group())
        layout.addWidget(_position_group())
        layout.addWidget(_import_group())
        layout.addStretch()
        self.setLayout(layout)
