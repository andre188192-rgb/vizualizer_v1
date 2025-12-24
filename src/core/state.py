"""State structures for CNC simulator kinematics."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MachineState:
    """Machine axis state for forward kinematics.

    Coordinates follow the machine coordinate system (MCS).

    Attributes:
        x: Linear X position in millimeters (MCS).
        y: Linear Y position in millimeters (MCS).
        z: Linear Z position in millimeters (MCS).
        tool_length_offset: Tool length offset H in millimeters along tool axis.

    Example:
        state = MachineState(x=100.0, y=50.0, z=-20.0, tool_length_offset=10.0)
    """

    x: float
    y: float
    z: float
    tool_length_offset: float


@dataclass(frozen=True)
class KinematicConfig:
    """Kinematic configuration for a machine.

    This placeholder is intentionally minimal for Sprint 1.

    Example:
        config = KinematicConfig()
    """

    pass
