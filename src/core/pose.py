"""Pose representation for CNC simulator kinematics."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class Pose:
    """Rigid transform from TCP (tool center point) to MCS.

    The pose follows the convention: p_mcs = T_mcs_from_tcp @ p_tcp,
    where vectors are 4x1 homogeneous column vectors.

    Attributes:
        T_mcs_from_tcp: 4x4 homogeneous transform matrix.

    Example:
        T = np.eye(4)
        pose = Pose(T)
        tcp_in_mcs = pose.transform_point(np.array([0, 0, 0, 1]))
    """

    T_mcs_from_tcp: np.ndarray
    _T_wcs_from_tcp: Optional[np.ndarray] = field(default=None, init=False, repr=False)

    def transform_point(self, p_tcp: np.ndarray) -> np.ndarray:
        """Transform a point from TCP coordinates to MCS.

        Args:
            p_tcp: Homogeneous point as a 4-element vector or 4x1 column vector.

        Returns:
            Homogeneous point in MCS as a 4-element vector.

        Example:
            point_mcs = pose.transform_point(np.array([0, 0, 0, 1]))
        """

        p_tcp_array = np.asarray(p_tcp, dtype=float)
        if p_tcp_array.shape == (4, 1):
            p_tcp_array = p_tcp_array[:, 0]
        if p_tcp_array.shape != (4,):
            raise ValueError("p_tcp must be a homogeneous 4-element vector")
        return self.T_mcs_from_tcp @ p_tcp_array

    def apply_to_gl(self, gl_mult_matrixf=None) -> None:
        """Load the pose matrix into OpenGL without axis reinterpretation.

        OpenGL expects column-major order. NumPy uses row-major by default,
        so the matrix is transposed before flattening.

        Args:
            gl_mult_matrixf: Optional OpenGL function for loading a matrix.
                If None, OpenGL.GL.glMultMatrixf is imported.

        Example:
            pose.apply_to_gl()
        """

        if gl_mult_matrixf is None:
            from OpenGL.GL import glMultMatrixf

            gl_mult_matrixf = glMultMatrixf
        gl_matrix = self.T_mcs_from_tcp.T.flatten()
        gl_mult_matrixf(gl_matrix)
