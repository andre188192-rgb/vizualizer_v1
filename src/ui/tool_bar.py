"""Tool bar configuration."""

from typing import Optional

from PyQt5.QtWidgets import QAction, QMainWindow


def _register_action(actions: dict[str, QAction], key: str, action: QAction) -> QAction:
    actions[key] = action
    return action


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


def build_tool_bar(window: QMainWindow) -> dict[str, QAction]:
    tool_bar = window.addToolBar("Main")
    tool_bar.setMovable(True)
    actions: dict[str, QAction] = {}

    tool_bar.addAction(
        _register_action(
            actions,
            "new_project",
            _action(window, "New", "Create a new simulation", "Ctrl+N"),
        )
    )
    tool_bar.addAction(
        _register_action(
            actions,
            "open_project",
            _action(window, "Open", "Open a project", "Ctrl+O"),
        )
    )
    tool_bar.addAction(
        _register_action(
            actions,
            "save_project",
            _action(window, "Save", "Save the current project", "Ctrl+S"),
        )
    )
    tool_bar.addSeparator()
    tool_bar.addAction(
        _register_action(
            actions,
            "play",
            _action(window, "Play", "Start simulation", "Space"),
        )
    )
    tool_bar.addAction(
        _register_action(actions, "pause", _action(window, "Pause", "Pause simulation"))
    )
    tool_bar.addAction(
        _register_action(
            actions,
            "stop",
            _action(window, "Stop", "Stop simulation", "Ctrl+Space"),
        )
    )
    return actions
