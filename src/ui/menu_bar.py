"""Menu bar configuration."""

from typing import Optional

from PyQt5.QtWidgets import QAction, QMainWindow


def _action(
    window: QMainWindow,
    title: str,
    status: str,
    shortcut: Optional[str] = None,
    checkable: bool = False,
) -> QAction:
    action = QAction(title, window)
    action.setStatusTip(status)
    if shortcut:
        action.setShortcut(shortcut)
    action.setCheckable(checkable)
    return action


def build_menu_bar(window: QMainWindow) -> None:
    menu_bar = window.menuBar()

    file_menu = menu_bar.addMenu("File")
    file_menu.addAction(_action(window, "New Simulation", "Create a new simulation", "Ctrl+N"))
    file_menu.addAction(_action(window, "Open Project", "Open a CNC project", "Ctrl+O"))
    file_menu.addAction(_action(window, "Save Project", "Save the current project", "Ctrl+S"))
    file_menu.addAction(_action(window, "Save As", "Save as a new project file", "Ctrl+Shift+S"))
    file_menu.addSeparator()
    file_menu.addAction(_action(window, "Recent Files", "View recent projects"))
    file_menu.addSeparator()
    file_menu.addAction(_action(window, "Exit", "Exit the application", "Ctrl+Q"))

    edit_menu = menu_bar.addMenu("Edit")
    edit_menu.addAction(_action(window, "Preferences", "Open application preferences"))
    edit_menu.addAction(_action(window, "Keyboard Shortcuts", "Edit shortcuts"))
    edit_menu.addAction(_action(window, "Reset Settings", "Reset preferences"))
    edit_menu.addSeparator()
    edit_menu.addAction(_action(window, "Undo", "Undo last action", "Ctrl+Z"))
    edit_menu.addAction(_action(window, "Redo", "Redo last action", "Ctrl+Y"))

    view_menu = menu_bar.addMenu("View")
    view_menu.addAction(_action(window, "Wireframe", "Toggle wireframe mode", checkable=True))
    view_menu.addAction(
        _action(window, "Show/Hide Workpiece", "Toggle workpiece visibility", checkable=True)
    )
    view_menu.addAction(
        _action(window, "Show/Hide Toolpath", "Toggle toolpath visibility", checkable=True)
    )
    view_menu.addAction(_action(window, "Camera Presets", "Select a camera preset"))
    view_menu.addAction(_action(window, "Reset View", "Reset the camera", "F5"))

    simulation_menu = menu_bar.addMenu("Simulation")
    simulation_menu.addAction(
        _action(window, "Play/Pause", "Start or pause simulation", "Space")
    )
    simulation_menu.addAction(
        _action(window, "Stop", "Stop simulation", "Ctrl+Space")
    )
    simulation_menu.addAction(_action(window, "Step Forward", "Advance one step", "]"))
    simulation_menu.addAction(_action(window, "Step Backward", "Go back one step", "["))
    simulation_menu.addAction(_action(window, "Set Speed", "Adjust playback speed"))

    tools_menu = menu_bar.addMenu("Tools")
    tools_menu.addAction(_action(window, "G-code Validator", "Validate G-code"))
    tools_menu.addAction(_action(window, "Collision Checker", "Check for collisions"))
    tools_menu.addAction(_action(window, "Post-processor", "Open post-processor"))

    help_menu = menu_bar.addMenu("Help")
    help_menu.addAction(_action(window, "Documentation", "Open documentation", "F1"))
    help_menu.addAction(_action(window, "About", "About the application"))
    help_menu.addAction(_action(window, "Check for Updates", "Check for updates"))
