"""Status bar configuration."""

from PyQt5.QtWidgets import QLabel, QMainWindow, QProgressBar


def build_status_bar(window: QMainWindow) -> None:
    status_bar = window.statusBar()

    left = QLabel("Ready | Project: demo.cncproj | Tool: Endmill 10mm")
    status_bar.addWidget(left, 2)

    center = QLabel("X: 123.4  Y: 56.7  Z: 89.0  A: 0.0  B: 0.0  C: 0.0")
    status_bar.addWidget(center, 3)

    progress = QProgressBar()
    progress.setRange(0, 100)
    progress.setValue(26)
    progress.setFormat("Simulation: %p%")
    progress.setMaximumWidth(200)
    status_bar.addPermanentWidget(progress, 1)

    right = QLabel("FPS: 60 | Memory: 245 MB | ⚡ | 14:30")
    status_bar.addPermanentWidget(right, 1)
