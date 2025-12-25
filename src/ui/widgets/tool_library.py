"""Tool library list widget."""

from PyQt5.QtWidgets import QListWidget


class ToolLibrary(QListWidget):
    """List showing available tools."""

    def __init__(self) -> None:
        super().__init__()
        self.addItems(
            [
                "Endmill 10mm (Flat)",
                "Endmill 6mm (Ball)",
                "Drill 5mm",
            ]
        )
