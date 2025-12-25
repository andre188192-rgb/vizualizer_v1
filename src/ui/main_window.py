"""Main window for the CNC Machine 3D Simulator Pro UI."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDockWidget,
    QListWidget,
    QMainWindow,
    QSplitter,
    QTabWidget,
    QWidget,
)

from .menu_bar import build_menu_bar
from .status_bar import build_status_bar
from .tool_bar import build_tool_bar
from .tabs.gcode_tab import GCodeTab
from .tabs.machine_tab import MachineTab
from .tabs.settings_tab import SettingsTab
from .tabs.simulation_tab import SimulationTab
from .tabs.tool_tab import ToolTab
from .tabs.workpiece_tab import WorkpieceTab
from .widgets.viewport_widget import ViewportWidget


class MainWindow(QMainWindow):
    """Primary application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("CNC Machine 3D Simulator Pro")
        self.setMinimumSize(1200, 800)

        build_menu_bar(self)
        build_tool_bar(self)
        build_status_bar(self)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._build_viewport())
        splitter.addWidget(self._build_control_panel())
        splitter.setStretchFactor(0, 7)
        splitter.setStretchFactor(1, 3)
        self.setCentralWidget(splitter)

        self.addDockWidget(Qt.RightDockWidgetArea, self._build_notifications_dock())

    def _build_viewport(self) -> QWidget:
        return ViewportWidget()

    def _build_control_panel(self) -> QWidget:
        tabs = QTabWidget()
        tabs.addTab(MachineTab(), "Machine Configuration")
        tabs.addTab(ToolTab(), "Tool Management")
        tabs.addTab(WorkpieceTab(), "Workpiece Setup")
        tabs.addTab(GCodeTab(), "G-code Control")
        tabs.addTab(SimulationTab(), "Simulation & Analysis")
        tabs.addTab(SettingsTab(), "Settings")
        return tabs

    def _build_notifications_dock(self) -> QDockWidget:
        dock = QDockWidget("Notifications", self)
        dock.setObjectName("notificationsDock")
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        list_widget = QListWidget()
        list_widget.addItems(
            [
                "Info: Project loaded successfully",
                "Warning: Toolpath exceeds X travel",
                "Error: Missing spindle model",
                "Success: G-code validation passed",
            ]
        )
        dock.setWidget(list_widget)
        return dock
