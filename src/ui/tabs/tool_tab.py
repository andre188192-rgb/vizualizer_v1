"""Tool management tab."""

from PyQt5.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..widgets.preview_widget import PreviewWidget
from ..widgets.tool_library import ToolLibrary


def _library_group() -> QGroupBox:
    group = QGroupBox("Tool Library")
    layout = QVBoxLayout()
    search = QLineEdit()
    search.setPlaceholderText("Search tools...")
    layout.addWidget(search)
    layout.addWidget(ToolLibrary())

    button_row = QHBoxLayout()
    button_row.addWidget(QPushButton("Create New"))
    button_row.addWidget(QPushButton("Edit"))
    button_row.addWidget(QPushButton("Delete"))
    layout.addLayout(button_row)

    group.setLayout(layout)
    return group


def _parameters_group() -> QGroupBox:
    group = QGroupBox("Tool Parameters")
    layout = QVBoxLayout()
    layout.addWidget(PreviewWidget(title="Tool Preview", subtitle=""))

    form = QFormLayout()
    tool_type = QComboBox()
    tool_type.addItems(["Flat Endmill", "Ball Endmill", "Drill", "Chamfer"])
    form.addRow("Type", tool_type)

    diameter = QDoubleSpinBox()
    diameter.setRange(0.1, 200.0)
    diameter.setValue(10.0)
    diameter.setSuffix(" mm")
    form.addRow("Diameter", diameter)

    length = QDoubleSpinBox()
    length.setRange(1.0, 500.0)
    length.setValue(50.0)
    length.setSuffix(" mm")
    form.addRow("Length", length)

    cutting = QDoubleSpinBox()
    cutting.setRange(1.0, 500.0)
    cutting.setValue(40.0)
    cutting.setSuffix(" mm")
    form.addRow("Cutting Length", cutting)

    shank = QDoubleSpinBox()
    shank.setRange(0.1, 200.0)
    shank.setValue(12.0)
    shank.setSuffix(" mm")
    form.addRow("Shank Diameter", shank)

    flutes = QSpinBox()
    flutes.setRange(1, 12)
    flutes.setValue(4)
    form.addRow("Flutes", flutes)
    layout.addLayout(form)

    button_row = QHBoxLayout()
    button_row.addWidget(QPushButton("Apply"))
    button_row.addWidget(QPushButton("Save to Library"))
    layout.addLayout(button_row)

    group.setLayout(layout)
    return group


class ToolTab(QWidget):
    """Tab for tool management."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(_library_group())
        layout.addWidget(_parameters_group())
        layout.addStretch()
        self.setLayout(layout)
