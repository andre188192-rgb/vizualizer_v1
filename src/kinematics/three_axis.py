"""Three-axis VMC forward kinematics."""
from __future__ import annotations

import numpy as np

from core.pose import Pose
from core.state import KinematicConfig, MachineState


def _translation(x: float, y: float, z: float) -> np.ndarray:
    """Create a homogeneous translation matrix.

    Args:
        x: Translation in X.
        y: Translation in Y.
        z: Translation in Z.

    Returns:
        4x4 homogeneous transform matrix.

    Example:
        T = _translation(1.0, 2.0, 3.0)
    """

    matrix = np.eye(4)
    matrix[:3, 3] = [x, y, z]
    return matrix


def forward_kinematics(state: MachineState, config: KinematicConfig) -> Pose:
    """Compute T_mcs_from_tcp for a 3-axis VMC.

    The tool axis is aligned with -Z in TCP coordinates. Tool length offset
    is applied as a translation along -Z in the spindle frame.

    Args:
        state: Current machine state (X/Y/Z and tool length offset).
        config: Kinematic configuration (unused in Sprint 1).

    Returns:
        Pose containing T_mcs_from_tcp.

    Example:
        pose = forward_kinematics(state, config)
        tcp_position = pose.transform_point(np.array([0, 0, 0, 1]))
    """

    _ = config
    T_mcs_from_spindle = _translation(state.x, state.y, state.z)
    T_spindle_from_tcp = _translation(0.0, 0.0, -state.tool_length_offset)
    T_mcs_from_tcp = T_mcs_from_spindle @ T_spindle_from_tcp
    return Pose(T_mcs_from_tcp)
