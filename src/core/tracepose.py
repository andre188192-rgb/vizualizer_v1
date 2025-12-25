"""Tracepose logging helpers."""
from __future__ import annotations

import json
import logging
from typing import Dict, Any

import numpy as np

from .pose import Pose
from .state import MachineState


def log_tracepose(state: MachineState, pose: Pose) -> None:
    """Log a structured TRACEPOSE entry for debugging.

    Args:
        state: Current machine state in MCS.
        pose: Pose containing T_mcs_from_tcp.

    Example:
        log_tracepose(state, pose)
    """

    tcp_position = pose.transform_point(np.array([0, 0, 0, 1]))
    log_entry: Dict[str, Any] = {
        "state_axes": {"X": state.x, "Y": state.y, "Z": state.z},
        "tool_offset": state.tool_length_offset,
        "T_mcs_from_tcp_translation": pose.T_mcs_from_tcp[:3, 3].tolist(),
        "tool_axis": pose.T_mcs_from_tcp[:3, 2].tolist(),
        "tcp_position_mcs": tcp_position[:3].tolist(),
    }
    logging.info(json.dumps(log_entry, default=str))
