"""Axis configuration table widget."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QTableWidgetItem


class AxisTable(QTableWidget):
    """Table showing configured axes."""

    def __init__(self) -> None:
        super().__init__(0, 5)
        self.setHorizontalHeaderLabels(["Active", "Axis", "Type", "Min", "Max"])
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        self._seed_rows()

    def _seed_rows(self) -> None:
        rows = [
            (True, "X", "Linear", "-250", "250"),
            (True, "Y", "Linear", "-200", "200"),
            (True, "Z", "Linear", "0", "300"),
            (False, "A", "Rotary", "-180", "180"),
        ]
        self.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            active_item = QTableWidgetItem()
            active_item.setCheckState(Qt.Checked if row[0] else Qt.Unchecked)
            active_item.setFlags(active_item.flags() & ~Qt.ItemIsEditable)
            self.setItem(row_index, 0, active_item)

            for col_index, value in enumerate(row[1:], start=1):
                self.setItem(row_index, col_index, QTableWidgetItem(value))
        self.resizeColumnsToContents()

    def get_axis_config(self) -> list[dict[str, str | bool]]:
        config: list[dict[str, str | bool]] = []
        for row in range(self.rowCount()):
            active_item = self.item(row, 0)
            config.append(
                {
                    "active": active_item.checkState() == Qt.Checked if active_item else False,
                    "axis": self.item(row, 1).text() if self.item(row, 1) else "",
                    "type": self.item(row, 2).text() if self.item(row, 2) else "",
                    "min": self.item(row, 3).text() if self.item(row, 3) else "0",
                    "max": self.item(row, 4).text() if self.item(row, 4) else "0",
                }
            )
        return config
