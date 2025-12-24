"""State and configuration structures for machine kinematics."""

from dataclasses import dataclass


@dataclass
class MachineState:
    """Machine axis positions and tool offsets.

    Attributes:
        x: Linear axis X position in millimeters (MCS).
        y: Linear axis Y position in millimeters (MCS).
        z: Linear axis Z position in millimeters (MCS).
        tool_length_offset: Tool length offset (H) in millimeters.
    """

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    tool_length_offset: float = 0.0


@dataclass
class KinematicConfig:
    """Kinematic configuration placeholder for future expansion."""

    pass
