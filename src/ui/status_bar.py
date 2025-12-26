"""Status bar configuration."""

from dataclasses import dataclass

from PyQt5.QtWidgets import QLabel, QMainWindow, QProgressBar


@dataclass
class StatusBarWidgets:
    """References to status bar widgets for updates."""

    left: QLabel
    center: QLabel
    right: QLabel
    progress: QProgressBar


def build_status_bar(window: QMainWindow) -> StatusBarWidgets:
    status_bar = window.statusBar()

    left = QLabel("Ready | Project: demo.cncproj | Tool: Endmill 10mm")
    status_bar.addWidget(left, 2)

    center = QLabel("X: 0.0  Y: 0.0  Z: 0.0  A: 0.0  B: 0.0  C: 0.0")
    status_bar.addWidget(center, 3)

    progress = QProgressBar()
    progress.setRange(0, 100)
    progress.setValue(0)
    progress.setFormat("Simulation: %p%")
    progress.setMaximumWidth(200)
    status_bar.addPermanentWidget(progress, 1)

    right = QLabel("FPS: 60 | Memory: 245 MB | ⚡ | 14:30")
    status_bar.addPermanentWidget(right, 1)

    return StatusBarWidgets(left=left, center=center, right=right, progress=progress)
