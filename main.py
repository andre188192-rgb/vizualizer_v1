"""PyQt application entrypoint for Vizualizer."""

import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parent
SRC_PATH = ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from ui.main_window import MainWindow


def main() -> int:
    """Launch the PyQt UI."""
    app = QApplication(sys.argv)
    window = MainWindow()
    qss_path = ROOT / "src" / "ui" / "styles" / "dark_theme.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
