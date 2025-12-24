import numpy as np

from src.core.pose import Pose


def test_pose_consumers_agreement():
    """All pose consumers should read identical TCP coordinates."""

    renderer_marker = []
    material_point = []

    def mock_renderer(pose: Pose) -> None:
        renderer_marker.append(pose.transform_point([0, 0, 0, 1]))

    def mock_material(pose: Pose) -> None:
        material_point.append(pose.transform_point([0, 0, 0, 1]))

    test_pose = Pose(np.eye(4))
    mock_renderer(test_pose)
    mock_material(test_pose)

    assert np.allclose(renderer_marker[0], material_point[0], atol=0.001)
