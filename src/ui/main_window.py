"""Main window for the CNC Machine 3D Simulator Pro UI."""

from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget, QMessageBox
from PyQt5.QtWidgets import QDockWidget, QMainWindow, QSplitter, QTabWidget, QWidget

from controller.machine_controller import AxisConfig, MachineController

from .menu_bar import build_menu_bar
from .status_bar import StatusBarWidgets, build_status_bar
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
from .widgets.gl_widget import GLWidget
from .widgets.viewport_widget import ViewportWidget


class MainWindow(QMainWindow):
    """Primary application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("CNC Machine 3D Simulator Pro")
        self.setMinimumSize(1200, 800)

        self.menu_actions = build_menu_bar(self)
        self.tool_actions = build_tool_bar(self)
        self.status_widgets = build_status_bar(self)
        build_menu_bar(self)
        build_tool_bar(self)
        build_status_bar(self)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._build_viewport())
        splitter.addWidget(self._build_control_panel())
        splitter.setStretchFactor(0, 7)
        splitter.setStretchFactor(1, 3)
        self.setCentralWidget(splitter)

        self.notifications_list = self._build_notifications_dock()
        self.addDockWidget(Qt.RightDockWidgetArea, self.notifications_list)

        self.controller = MachineController()
        self._connect_controller()
        self._connect_ui_actions()

    def _build_viewport(self) -> QWidget:
        self.gl_widget = GLWidget()
        return self.gl_widget
        self.addDockWidget(Qt.RightDockWidgetArea, self._build_notifications_dock())

    def _build_viewport(self) -> QWidget:
        return ViewportWidget()

    def _build_control_panel(self) -> QWidget:
        tabs = QTabWidget()
        self.machine_tab = MachineTab()
        self.tool_tab = ToolTab()
        self.workpiece_tab = WorkpieceTab()
        self.gcode_tab = GCodeTab()
        self.simulation_tab = SimulationTab()
        self.settings_tab = SettingsTab()

        tabs.addTab(self.machine_tab, "Machine Configuration")
        tabs.addTab(self.tool_tab, "Tool Management")
        tabs.addTab(self.workpiece_tab, "Workpiece Setup")
        tabs.addTab(self.gcode_tab, "G-code Control")
        tabs.addTab(self.simulation_tab, "Simulation & Analysis")
        tabs.addTab(self.settings_tab, "Settings")
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
        self.notifications_widget = list_widget
        return dock

    def _connect_controller(self) -> None:
        self.controller.simulation_progress.connect(self._update_simulation_progress)
        self.controller.machine_state_changed.connect(self._update_machine_state)
        self.controller.error_occurred.connect(self._show_error)
        self.controller.gcode_loaded.connect(self._on_gcode_loaded)

    def _connect_ui_actions(self) -> None:
        machine_tab = self._machine_tab()
        machine_tab.apply_button.clicked.connect(self._apply_axis_config)
        for axis, slider in machine_tab.axis_sliders.items():
            slider.valueChanged.connect(
                lambda value, axis_name=axis: self._on_axis_slider_changed(axis_name, value)
            )

        tool_tab = self._tool_tab()
        tool_tab.apply_button.clicked.connect(self._apply_tool_params)

        workpiece_tab = self._workpiece_tab()
        workpiece_tab.reset_button.clicked.connect(self._apply_workpiece)

        gcode_tab = self._gcode_tab()
        gcode_tab.load_button.clicked.connect(self._load_gcode_file)
        gcode_tab.save_button.clicked.connect(self._save_gcode_file)
        gcode_tab.validate_button.clicked.connect(self._apply_gcode_text)
        gcode_tab.start_button.clicked.connect(self._start_simulation)
        gcode_tab.pause_button.clicked.connect(self.controller.pause_simulation)
        gcode_tab.stop_button.clicked.connect(self.controller.stop_simulation)

        self.menu_actions["open_project"].triggered.connect(self._load_gcode_file)
        self.menu_actions["save_project"].triggered.connect(self._save_gcode_file)
        self.menu_actions["save_as"].triggered.connect(self._save_gcode_file)
        self.menu_actions["new_project"].triggered.connect(self._new_project_stub)
        self.menu_actions["exit"].triggered.connect(self.close)
        self.menu_actions["play_pause"].triggered.connect(self._toggle_play_pause)
        self.menu_actions["stop_sim"].triggered.connect(self.controller.stop_simulation)

        self.tool_actions["open_project"].triggered.connect(self._load_gcode_file)
        self.tool_actions["save_project"].triggered.connect(self._save_gcode_file)
        self.tool_actions["new_project"].triggered.connect(self._new_project_stub)
        self.tool_actions["play"].triggered.connect(self._start_simulation)
        self.tool_actions["pause"].triggered.connect(self.controller.pause_simulation)
        self.tool_actions["stop"].triggered.connect(self.controller.stop_simulation)

    def _machine_tab(self) -> MachineTab:
        return self.machine_tab

    def _tool_tab(self) -> ToolTab:
        return self.tool_tab

    def _workpiece_tab(self) -> WorkpieceTab:
        return self.workpiece_tab

    def _gcode_tab(self) -> GCodeTab:
        return self.gcode_tab

    def _apply_axis_config(self) -> None:
        tab = self._machine_tab()
        axis_config = []
        for row in tab.get_axis_configuration():
            try:
                axis_config.append(
                    AxisConfig(
                        name=row["axis"],
                        axis_type=row["type"],
                        minimum=float(row["min"]),
                        maximum=float(row["max"]),
                        active=bool(row["active"]),
                    )
                )
            except ValueError:
                self._show_error("Validation", "Axis limits must be numeric.")
                return
        self.controller.apply_axis_configuration(axis_config)

    def _apply_tool_params(self) -> None:
        tab = self._tool_tab()
        self.controller.apply_tool_parameters(tab.get_tool_parameters())

    def _apply_workpiece(self) -> None:
        tab = self._workpiece_tab()
        self.controller.create_workpiece(tab.get_workpiece_parameters())

    def _apply_gcode_text(self) -> None:
        tab = self._gcode_tab()
        self.controller.load_gcode_text(tab.gcode_text())

    def _load_gcode_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open G-code", "", "G-code Files (*.nc *.tap *.gcode *.txt)"
        )
        if file_path:
            self.controller.load_gcode_file(Path(file_path))
            self._gcode_tab().set_gcode_text(self.controller.current_gcode())
            self._show_info("G-code Loaded", f"Loaded file: {file_path}")

    def _save_gcode_file(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save G-code", "", "G-code Files (*.nc *.tap *.gcode *.txt)"
        )
        if file_path:
            Path(file_path).write_text(self._gcode_tab().gcode_text(), encoding="utf-8")
            self._show_info("G-code Saved", f"Saved file: {file_path}")

    def _start_simulation(self) -> None:
        gcode_tab = self._gcode_tab()
        self.controller.start_simulation(gcode_tab.speed_slider.value())
        self._show_info("Simulation", "Simulation started.")

    def _toggle_play_pause(self) -> None:
        if self.controller.is_simulation_running():
            self.controller.pause_simulation()
            self._show_info("Simulation", "Simulation paused.")
        else:
            self._start_simulation()

    def _update_simulation_progress(self, current: int, total: int) -> None:
        self._gcode_tab().set_progress(current, total)
        self.status_widgets.progress.setMaximum(max(total, 1))
        self.status_widgets.progress.setValue(current)

    def _update_machine_state(self, positions: dict) -> None:
        axis_values = "  ".join(
            f"{axis}: {value:.1f}" for axis, value in sorted(positions.items())
        )
        self.status_widgets.center.setText(axis_values)
        machine_tab = self._machine_tab()
        for axis, value in positions.items():
            slider = machine_tab.axis_sliders.get(axis)
            label = machine_tab.axis_labels.get(axis)
            if slider:
                slider.blockSignals(True)
                slider.setValue(int(value))
                slider.blockSignals(False)
            if label:
                label.setText(f"{value:.1f}")
            self.gl_widget.set_axis_position(axis, float(value))

    def _on_gcode_loaded(self, count: int) -> None:
        self.notifications_widget.addItem(f"Info: Loaded {count} G-code commands")

    def _show_error(self, title: str, message: str) -> None:
        self.notifications_widget.addItem(f"Error: {title} - {message}")
        QMessageBox.warning(self, title, message)

    def _on_axis_slider_changed(self, axis: str, value: int) -> None:
        self.controller.set_axis_position(axis, float(value))

    def _show_info(self, title: str, message: str) -> None:
        self.notifications_widget.addItem(f"Info: {title} - {message}")
        QMessageBox.information(self, title, message)

    def _new_project_stub(self) -> None:
        self._show_info("New Project", "Project creation is not implemented yet.")
        return dock
