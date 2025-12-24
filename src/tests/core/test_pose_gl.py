import numpy as np

from src.core.pose import Pose


def test_to_gl_array_is_column_major():
    """OpenGL array should be column-major (transpose of NumPy)."""

    matrix = np.array(
        [
            [1.0, 2.0, 3.0, 4.0],
            [5.0, 6.0, 7.0, 8.0],
            [9.0, 10.0, 11.0, 12.0],
            [13.0, 14.0, 15.0, 16.0],
        ]
    )
    pose = Pose(matrix)
    gl_array = pose.to_gl_array()
    expected = matrix.T.flatten()
    assert np.array_equal(gl_array, expected)
