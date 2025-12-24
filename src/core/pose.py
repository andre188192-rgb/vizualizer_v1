"""Pose contract and transformation helpers for CNC kinematics."""

from __future__ import annotations

from typing import Optional

import numpy as np


class Pose:
    """Pose holding the TCP transformation matrix.

    The matrix follows the convention:
        p_mcs = T_mcs_from_tcp @ p_tcp

    Args:
        T_mcs_from_tcp: 4x4 homogeneous transform from TCP to MCS.
    """

    def __init__(self, T_mcs_from_tcp: np.ndarray) -> None:
        self.T_mcs_from_tcp = np.asarray(T_mcs_from_tcp, dtype=float)
        self._T_wcs_from_tcp: Optional[np.ndarray] = None

    def transform_point(self, p_tcp: np.ndarray) -> np.ndarray:
        """Transform a point from TCP/TCS to MCS.

        Args:
            p_tcp: Homogeneous point [x, y, z, 1] in TCP coordinates.

        Returns:
            Homogeneous point in MCS coordinates.

        Example:
            >>> pose = Pose(np.eye(4))
            >>> pose.transform_point([0, 0, 0, 1])
        """

        return self.T_mcs_from_tcp @ np.asarray(p_tcp, dtype=float)

    def to_gl_array(self) -> np.ndarray:
        """Return the column-major matrix array for OpenGL.

        Returns:
            Flattened 16-element array in column-major order.

        Example:
            >>> pose = Pose(np.eye(4))
            >>> pose.to_gl_array().shape
            (16,)
        """

        return self.T_mcs_from_tcp.T.flatten()

    def apply_to_gl(self) -> None:
        """Load the pose matrix into OpenGL.

        OpenGL expects column-major matrices, so the matrix is transposed
        before loading.

        Example:
            >>> pose = Pose(np.eye(4))
            >>> pose.apply_to_gl()  # doctest: +SKIP
        """

        from OpenGL.GL import glMultMatrixf

        glMultMatrixf(self.to_gl_array())
