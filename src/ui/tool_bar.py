"""Tool bar configuration."""

from typing import Optional

from PyQt5.QtWidgets import QAction, QMainWindow


def _action(
    window: QMainWindow,
    title: str,
    tooltip: str,
    shortcut: Optional[str] = None,
) -> QAction:
    action = QAction(title, window)
    action.setToolTip(tooltip)
    if shortcut:
        action.setShortcut(shortcut)
    return action


def build_tool_bar(window: QMainWindow) -> None:
    tool_bar = window.addToolBar("Main")
    tool_bar.setMovable(True)

    tool_bar.addAction(_action(window, "New", "Create a new simulation", "Ctrl+N"))
    tool_bar.addAction(_action(window, "Open", "Open a project", "Ctrl+O"))
    tool_bar.addAction(_action(window, "Save", "Save the current project", "Ctrl+S"))
    tool_bar.addSeparator()
    tool_bar.addAction(_action(window, "Play", "Start simulation", "Space"))
    tool_bar.addAction(_action(window, "Pause", "Pause simulation"))
    tool_bar.addAction(_action(window, "Stop", "Stop simulation", "Ctrl+Space"))
    tool_bar.addAction(_action(window, "Step +", "Step forward", "]"))
    tool_bar.addAction(_action(window, "Step -", "Step backward", "["))
    tool_bar.addSeparator()
    tool_bar.addAction(_action(window, "Measure", "Measure toolpath"))
    tool_bar.addAction(_action(window, "Alerts", "Review alerts"))
    tool_bar.addAction(_action(window, "Zoom", "Zoom to selection"))
    tool_bar.addSeparator()
    tool_bar.addAction(_action(window, "Settings", "Open settings"))
