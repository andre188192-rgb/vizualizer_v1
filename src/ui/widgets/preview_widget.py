"""Preview widget for placeholders."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QWidget


class PreviewWidget(QWidget):
    """Reusable placeholder card for previews."""

    def __init__(self, title: str, subtitle: str) -> None:
        super().__init__()
        frame = QFrame()
        frame.setObjectName("previewFrame")
        frame.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("previewTitle")
        layout.addWidget(title_label)

        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setAlignment(Qt.AlignCenter)
            subtitle_label.setObjectName("previewSubtitle")
            layout.addWidget(subtitle_label)

        frame.setLayout(layout)

        wrapper = QVBoxLayout()
        wrapper.addWidget(frame)
        self.setLayout(wrapper)
