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


def _dimensions_group() -> tuple[
    QGroupBox,
    dict[str, QDoubleSpinBox],
    QComboBox,
    QComboBox,
]:
    group = QGroupBox("Dimensions & Material")
    form = QFormLayout()
    fields: dict[str, QDoubleSpinBox] = {}
def _dimensions_group() -> QGroupBox:
    group = QGroupBox("Dimensions & Material")
    form = QFormLayout()
    for label, value in (("Width", 200.0), ("Height", 100.0), ("Depth", 50.0)):
        spin = QDoubleSpinBox()
        spin.setRange(1.0, 2000.0)
        spin.setValue(value)
        spin.setSuffix(" mm")
        form.addRow(label, spin)
        fields[label] = spin

    material = QComboBox()
    material.addItems(["Aluminum", "Steel", "Wood", "Plastic"])
    form.addRow("Material", material)

    color_button = QPushButton("Choose color")
    form.addRow("Color", color_button)

    zero_point = QComboBox()
    zero_point.addItems(["Top Center", "Top Left", "Bottom Center"])
    form.addRow("Zero Point", zero_point)
    group.setLayout(form)
    return group, fields, material, zero_point


def _position_group() -> tuple[QGroupBox, dict[str, QSlider]]:
    group = QGroupBox("Position")
    layout = QVBoxLayout()
    sliders: dict[str, QSlider] = {}
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
        sliders[axis] = slider
        layout.addLayout(row)

    group.setLayout(layout)
    return group, sliders


def _import_group() -> tuple[QGroupBox, QPushButton, QPushButton, QPushButton]:
    group = QGroupBox("Import / Export")
    layout = QHBoxLayout()
    import_button = QPushButton("Import STL")
    export_button = QPushButton("Export as STL")
    reset_button = QPushButton("Reset Workpiece")
    layout.addWidget(import_button)
    layout.addWidget(export_button)
    layout.addWidget(reset_button)
    group.setLayout(layout)
    return group, import_button, export_button, reset_button
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
        self.dimensions_group, self.dimension_fields, self.material_combo, self.zero_combo = (
            _dimensions_group()
        )
        self.position_group, self.position_sliders = _position_group()
        self.import_group, self.import_button, self.export_button, self.reset_button = (
            _import_group()
        )

        layout = QVBoxLayout()
        layout.addWidget(self.dimensions_group)
        layout.addWidget(self.position_group)
        layout.addWidget(self.import_group)
        layout.addStretch()
        self.setLayout(layout)

    def get_workpiece_parameters(self) -> dict[str, float | str]:
        return {
            "width": self.dimension_fields["Width"].value(),
            "height": self.dimension_fields["Height"].value(),
            "depth": self.dimension_fields["Depth"].value(),
            "material": self.material_combo.currentText(),
            "zero_point": self.zero_combo.currentText(),
            "position": {axis: slider.value() for axis, slider in self.position_sliders.items()},
        }
        layout = QVBoxLayout()
        layout.addWidget(_dimensions_group())
        layout.addWidget(_position_group())
        layout.addWidget(_import_group())
        layout.addStretch()
        self.setLayout(layout)
