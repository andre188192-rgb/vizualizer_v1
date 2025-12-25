"""Machine configuration tab."""

from PyQt5.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..widgets.axis_table import AxisTable


def _dimensions_group() -> QGroupBox:
    group = QGroupBox("Machine Envelope")
    form = QFormLayout()
    for axis, value in (("X (mm)", 500.0), ("Y (mm)", 400.0), ("Z (mm)", 300.0)):
        spin = QDoubleSpinBox()
        spin.setRange(0, 5000)
        spin.setValue(value)
        spin.setSuffix(" mm")
        spin.setDecimals(1)
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
        layout = QVBoxLayout()
        layout.addWidget(_dimensions_group())
        layout.addWidget(_axes_group())
        layout.addWidget(_structure_group())
        layout.addStretch()
        self.setLayout(layout)
