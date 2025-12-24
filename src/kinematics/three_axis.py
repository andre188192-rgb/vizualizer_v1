"""Forward kinematics for a 3-axis VMC."""

from __future__ import annotations

import numpy as np

from src.core.pose import Pose
from src.core.state import KinematicConfig, MachineState


def translation(x: float, y: float, z: float) -> np.ndarray:
    """Create a homogeneous translation matrix.

    Args:
        x: Translation along X axis in millimeters.
        y: Translation along Y axis in millimeters.
        z: Translation along Z axis in millimeters.

    Returns:
        4x4 homogeneous transform matrix.
    """

    matrix = np.eye(4)
    matrix[:3, 3] = [x, y, z]
    return matrix


def forward_kinematics(state: MachineState, config: KinematicConfig) -> Pose:
    """Compute T_mcs_from_tcp for a 3-axis VMC.

    This accounts for:
        - Linear X/Y/Z positions
        - Tool length offset (H) as translation along tool -Z

    Args:
        state: MachineState with axis positions and tool offset.
        config: KinematicConfig placeholder for future extensions.

    Returns:
        Pose containing T_mcs_from_tcp.
    """

    _ = config
    T_mcs_from_spindle = translation(state.x, state.y, state.z)
    T_spindle_from_tcp = translation(0.0, 0.0, -state.tool_length_offset)
    T_mcs_from_tcp = T_mcs_from_spindle @ T_spindle_from_tcp
    return Pose(T_mcs_from_tcp)
