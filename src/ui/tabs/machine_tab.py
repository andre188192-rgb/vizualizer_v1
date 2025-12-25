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


def _dimensions_group() -> tuple[QGroupBox, dict[str, QDoubleSpinBox]]:
    group = QGroupBox("Machine Envelope")
    form = QFormLayout()
    fields: dict[str, QDoubleSpinBox] = {}
    for axis, value in (("X", 500.0), ("Y", 400.0), ("Z", 300.0)):
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

    button_row = QHBoxLayout()
    button_row.addWidget(QPushButton("Add Axis"))
    button_row.addWidget(QPushButton("Remove Axis"))
    button_row.addStretch()
    save_button = QPushButton("Save Config")
    button_row.addWidget(save_button)
    layout.addLayout(button_row)

    group.setLayout(layout)
    return group, axis_table, save_button


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
        self.structure_group = _structure_group()

        layout = QVBoxLayout()
        layout.addWidget(self.dimensions_group)
        layout.addWidget(self.axes_group)
        layout.addWidget(self.structure_group)
        layout.addStretch()
        self.setLayout(layout)

    def get_dimension_values(self) -> dict[str, float]:
        return {key: widget.value() for key, widget in self.dimension_fields.items()}

    def get_axis_configuration(self) -> list[dict[str, str | bool]]:
        return self.axis_table.get_axis_config()
