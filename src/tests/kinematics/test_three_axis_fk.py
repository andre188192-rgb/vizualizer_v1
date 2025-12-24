import numpy as np

from src.core.state import KinematicConfig, MachineState
from src.kinematics.three_axis import forward_kinematics


def test_tool_length_offset():
    """TCP should be translated along tool -Z by tool length offset."""

    state = MachineState(x=0, y=0, z=0, tool_length_offset=30)
    config = KinematicConfig()
    pose = forward_kinematics(state, config)
    tcp_position = pose.transform_point([0, 0, 0, 1])
    expected = np.array([0, 0, -30, 1])
    assert np.allclose(tcp_position, expected, atol=0.01)


def test_xyz_movement():
    """TCP should reflect axis translations plus tool offset."""

    state = MachineState(x=100, y=50, z=-20, tool_length_offset=10)
    config = KinematicConfig()
    pose = forward_kinematics(state, config)
    tcp_position = pose.transform_point([0, 0, 0, 1])
    expected = np.array([100, 50, -30, 1])
    assert np.allclose(tcp_position, expected, atol=0.01)
