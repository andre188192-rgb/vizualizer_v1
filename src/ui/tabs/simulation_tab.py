"""Simulation and analysis tab."""

from PyQt5.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def _stats_group() -> QGroupBox:
    group = QGroupBox("Statistics")
    form = QFormLayout()
    form.addRow("Total time", QLabel("00:12:34"))
    form.addRow("Processed commands", QLabel("120/450 (26%)"))
    form.addRow("Removed material", QLabel("125 cm³"))
    form.addRow("Max X load", QLabel("85%"))
    form.addRow("Estimated remaining", QLabel("00:32:18"))
    group.setLayout(form)
    return group


def _visual_group() -> QGroupBox:
    group = QGroupBox("Visualization")
    layout = QVBoxLayout()
    show_toolpath = QCheckBox("Show toolpath")
    show_toolpath.setChecked(True)
    layout.addWidget(show_toolpath)
    show_cutting = QCheckBox("Show cutting zone")
    show_cutting.setChecked(True)
    layout.addWidget(show_cutting)
    layout.addWidget(QCheckBox("Show force vectors"))
    layout.addWidget(QCheckBox("Heatmap loads"))
    group.setLayout(layout)
    return group


def _analysis_group() -> QGroupBox:
    group = QGroupBox("Analysis")
    layout = QHBoxLayout()
    layout.addWidget(QPushButton("Collision Check"))
    layout.addWidget(QPushButton("Cycle Time Analysis"))
    layout.addWidget(QPushButton("Report Generator"))
    group.setLayout(layout)
    return group


class SimulationTab(QWidget):
    """Tab for simulation and analysis."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(_stats_group())
        layout.addWidget(_visual_group())
        layout.addWidget(_analysis_group())
        layout.addStretch()
        self.setLayout(layout)
