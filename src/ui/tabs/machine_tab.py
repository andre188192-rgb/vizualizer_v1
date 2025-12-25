"""Machine configuration tab."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..widgets.axis_table import AxisTable


def _dimensions_group() -> tuple[QGroupBox, dict[str, QDoubleSpinBox]]:
    group = QGroupBox("Machine Envelope")
    form = QFormLayout()
    fields: dict[str, QDoubleSpinBox] = {}
    for axis, value in (("X", 500.0), ("Y", 400.0), ("Z", 300.0)):
def _dimensions_group() -> QGroupBox:
    group = QGroupBox("Machine Envelope")
    form = QFormLayout()
    for axis, value in (("X (mm)", 500.0), ("Y (mm)", 400.0), ("Z (mm)", 300.0)):
        spin = QDoubleSpinBox()
        spin.setRange(0, 5000)
        spin.setValue(value)
        spin.setSuffix(" mm")
        spin.setDecimals(1)
        form.addRow(f"{axis} (mm)", spin)
        fields[axis] = spin
    group.setLayout(form)
    return group, fields


def _axes_group() -> tuple[QGroupBox, AxisTable, QPushButton]:
    group = QGroupBox("Axis Configuration")
    layout = QVBoxLayout()
    axis_table = AxisTable()
    layout.addWidget(axis_table)
        form.addRow(axis, spin)
    group.setLayout(form)
    return group


def _axes_group() -> QGroupBox:
    group = QGroupBox("Axis Configuration")
    layout = QVBoxLayout()
    layout.addWidget(AxisTable())

    button_row = QHBoxLayout()
    button_row.addWidget(QPushButton("Add Axis"))
    button_row.addWidget(QPushButton("Remove Axis"))
    button_row.addStretch()
    save_button = QPushButton("Save Config")
    button_row.addWidget(save_button)
    layout.addLayout(button_row)

    group.setLayout(layout)
    return group, axis_table, save_button


def _axis_position_group() -> tuple[QGroupBox, dict[str, QSlider], dict[str, QLabel]]:
    group = QGroupBox("Axis Positions")
    layout = QVBoxLayout()
    sliders: dict[str, QSlider] = {}
    labels: dict[str, QLabel] = {}

    for axis, minimum, maximum in (("X", -250, 250), ("Y", -200, 200), ("Z", 0, 300)):
        row = QHBoxLayout()
        row.addWidget(QLabel(f"{axis}:"))
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(0)
        value_label = QLabel("0")
        row.addWidget(slider)
        row.addWidget(value_label)
        layout.addLayout(row)
        sliders[axis] = slider
        labels[axis] = value_label

    group.setLayout(layout)
    return group, sliders, labels
    button_row.addWidget(QPushButton("Save Config"))
    layout.addLayout(button_row)

    group.setLayout(layout)
    return group


def _structure_group() -> QGroupBox:
    group = QGroupBox("Machine Structure")
    layout = QVBoxLayout()
    layout.addWidget(QCheckBox("Use 3D models"))

    button_row = QHBoxLayout()
    button_row.addWidget(QPushButton("Load Base"))
    button_row.addWidget(QPushButton("Load Columns"))
    button_row.addWidget(QPushButton("Load Spindle"))
    button_row.addWidget(QPushButton("Load Table"))
    layout.addLayout(button_row)

    group.setLayout(layout)
    return group


class MachineTab(QWidget):
    """Tab for machine configuration."""

    def __init__(self) -> None:
        super().__init__()
        self.dimensions_group, self.dimension_fields = _dimensions_group()
        self.axes_group, self.axis_table, self.apply_button = _axes_group()
        self.axis_position_group, self.axis_sliders, self.axis_labels = _axis_position_group()
        self.structure_group = _structure_group()

        layout = QVBoxLayout()
        layout.addWidget(self.dimensions_group)
        layout.addWidget(self.axes_group)
        layout.addWidget(self.axis_position_group)
        layout.addWidget(self.structure_group)
        layout.addStretch()
        self.setLayout(layout)

    def get_dimension_values(self) -> dict[str, float]:
        return {key: widget.value() for key, widget in self.dimension_fields.items()}

    def get_axis_configuration(self) -> list[dict[str, str | bool]]:
        return self.axis_table.get_axis_config()
        layout = QVBoxLayout()
        layout.addWidget(_dimensions_group())
        layout.addWidget(_axes_group())
        layout.addWidget(_structure_group())
        layout.addStretch()
        self.setLayout(layout)
