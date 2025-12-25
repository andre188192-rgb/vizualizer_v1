"""Viewport placeholder widget with overlays."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class ViewportWidget(QWidget):
    """Placeholder widget representing the OpenGL viewport."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("viewportWidget")

        frame = QFrame()
        frame.setObjectName("viewportFrame")
        frame.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 16, 16, 16)

        header = QLabel("3D View (OpenGL placeholder)")
        header.setObjectName("viewportTitle")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        hint = QLabel("Rotate: Left mouse | Pan: Middle mouse | Zoom: Wheel")
        hint.setObjectName("viewportHint")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        overlay = QLabel(
            "X: 123.4 mm  Y: 56.7 mm  Z: 89.0 mm\n"
            "F: 1500 mm/min  S: 10000 RPM\n"
            "Time: 00:12:34 / 00:45:12"
        )
        overlay.setObjectName("viewportOverlay")
        overlay.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(overlay)
        layout.addStretch()

        wrapper = QVBoxLayout()
        wrapper.addWidget(frame)
        self.setLayout(wrapper)
