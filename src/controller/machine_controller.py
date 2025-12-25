"""Controller to bridge UI interactions with simulator state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from PyQt5.QtCore import QObject, QTimer, pyqtSignal


@dataclass
class AxisConfig:
    """Axis configuration as defined by the UI."""

    name: str
    axis_type: str
    minimum: float
    maximum: float
    active: bool


class ValidationError(Exception):
    """Validation error for user input."""


class InputValidator:
    """Shared validation helpers for UI input."""

    @staticmethod
    def validate_axis_limits(min_val: float, max_val: float) -> None:
        if min_val >= max_val:
            raise ValidationError("Minimum value must be less than maximum.")

    @staticmethod
    def validate_tool_parameters(params: Dict[str, float]) -> None:
        if params["diameter"] <= 0:
            raise ValidationError("Tool diameter must be positive.")
        if params["length"] < params["cutting_length"]:
            raise ValidationError("Tool length must exceed cutting length.")


class MachineController(QObject):
    """Controller that stores and updates machine-related state."""

    simulation_started = pyqtSignal()
    simulation_paused = pyqtSignal()
    simulation_stopped = pyqtSignal()
    simulation_progress = pyqtSignal(int, int)
    machine_state_changed = pyqtSignal(dict)
    error_occurred = pyqtSignal(str, str)
    workpiece_updated = pyqtSignal()
    tool_changed = pyqtSignal()
    gcode_loaded = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self._axis_config: List[AxisConfig] = []
        self._tool_params: Dict[str, float | str] = {}
        self._workpiece_params: Dict[str, float | str] = {}
        self._gcode_lines: List[str] = []
        self._simulation_timer = QTimer()
        self._simulation_timer.setInterval(50)
        self._simulation_timer.timeout.connect(self._advance_simulation)
        self._simulation_current = 0

    def apply_axis_configuration(self, config: List[AxisConfig]) -> None:
        try:
            for axis in config:
                InputValidator.validate_axis_limits(axis.minimum, axis.maximum)
            self._axis_config = config
            self._emit_machine_state()
        except ValidationError as exc:
            self.error_occurred.emit("Validation", str(exc))

    def apply_tool_parameters(self, params: Dict[str, float | str]) -> None:
        try:
            InputValidator.validate_tool_parameters(
                {
                    "diameter": float(params["diameter"]),
                    "length": float(params["length"]),
                    "cutting_length": float(params["cutting_length"]),
                }
            )
            self._tool_params = params
            self.tool_changed.emit()
        except ValidationError as exc:
            self.error_occurred.emit("Validation", str(exc))

    def create_workpiece(self, params: Dict[str, float | str]) -> None:
        self._workpiece_params = params
        self.workpiece_updated.emit()

    def load_gcode_text(self, text: str) -> None:
        self._gcode_lines = [line for line in text.splitlines() if line.strip()]
        self._simulation_current = 0
        self.gcode_loaded.emit(len(self._gcode_lines))

    def load_gcode_file(self, filepath: Path) -> None:
        try:
            content = filepath.read_text(encoding="utf-8")
        except OSError as exc:
            self.error_occurred.emit("File error", str(exc))
            return
        self.load_gcode_text(content)

    def start_simulation(self, speed: int = 100) -> None:
        if not self._gcode_lines:
            self.error_occurred.emit("Simulation", "Load G-code before starting.")
            return
        self._simulation_timer.setInterval(max(10, int(200 - speed)))
        if not self._simulation_timer.isActive():
            self.simulation_started.emit()
            self._simulation_timer.start()

    def pause_simulation(self) -> None:
        if self._simulation_timer.isActive():
            self._simulation_timer.stop()
            self.simulation_paused.emit()

    def stop_simulation(self) -> None:
        if self._simulation_timer.isActive():
            self._simulation_timer.stop()
        self._simulation_current = 0
        self.simulation_stopped.emit()
        self.simulation_progress.emit(0, len(self._gcode_lines))

    def is_simulation_running(self) -> bool:
        return self._simulation_timer.isActive()

    def _advance_simulation(self) -> None:
        total = len(self._gcode_lines)
        if self._simulation_current >= total:
            self.stop_simulation()
            return
        self._simulation_current += 1
        self.simulation_progress.emit(self._simulation_current, total)
        self._emit_machine_state()

    def _emit_machine_state(self) -> None:
        positions = {axis.name: 0.0 for axis in self._axis_config if axis.active}
        positions.setdefault("X", 0.0)
        positions.setdefault("Y", 0.0)
        positions.setdefault("Z", 0.0)
        self.machine_state_changed.emit(positions)

    def current_gcode(self) -> str:
        return "\n".join(self._gcode_lines)
