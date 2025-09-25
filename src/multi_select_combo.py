from PySide6.QtWidgets import (
    QComboBox, QListWidget, QListWidgetItem, QCheckBox,
    QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QFrame
)
from PySide6.QtCore import Signal, Qt
from typing import List


class MultiSelectComboBox(QComboBox):
    selectionChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(35)

        # Create custom popup widget
        self.popup_widget = QWidget()
        self.popup_widget.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.popup_widget.setStyleSheet("""
            QWidget {
                background-color: #333333;
                border: 1px solid #404040;
                border-radius: 6px;
            }
        """)

        popup_layout = QVBoxLayout(self.popup_widget)
        popup_layout.setContentsMargins(5, 5, 5, 5)
        popup_layout.setSpacing(2)

        # List widget for checkboxes
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #333333;
                border: none;
                outline: none;
            }
        """)
        popup_layout.addWidget(self.list_widget)

        # Close button
        self.close_button = QPushButton("닫기")
        self.close_button.setMinimumHeight(25)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                border: none;
                border-radius: 3px;
                color: white;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
        """)
        self.close_button.clicked.connect(self.close_popup)
        popup_layout.addWidget(self.close_button)

        self.items = []
        self.selected_items = []

    def add_items(self, items: List[str]):
        self.items = items
        self.list_widget.clear()

        for item in items:
            list_item = QListWidgetItem()
            checkbox = QCheckBox(item)
            checkbox.stateChanged.connect(self.on_item_changed)

            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, checkbox)

    def on_item_changed(self):
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            checkbox = self.list_widget.itemWidget(item)
            if checkbox.isChecked():
                selected.append(checkbox.text())

        self.selected_items = selected
        self.update_display_text()
        self.selectionChanged.emit(selected)

    def update_display_text(self):
        if not self.selected_items:
            self.setCurrentText("요일을 선택하세요...")
        elif len(self.selected_items) == 1:
            self.setCurrentText(self.selected_items[0])
        else:
            text = f"{self.selected_items[0]} 외 {len(self.selected_items)-1}개"
            self.setCurrentText(text)

    def get_selected_items(self) -> List[str]:
        return self.selected_items.copy()

    def set_selected_items(self, items: List[str]):
        self.selected_items = items.copy()

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            checkbox = self.list_widget.itemWidget(item)
            checkbox.setChecked(checkbox.text() in items)

        self.update_display_text()

    def clear_selection(self):
        self.set_selected_items([])

    def close_popup(self):
        """Close the popup window"""
        self.popup_widget.hide()

    def hidePopup(self):
        """Override to use custom popup"""
        self.popup_widget.hide()

    def showPopup(self):
        """Show custom popup instead of default"""
        if self.popup_widget.isVisible():
            self.popup_widget.hide()
            return

        # Position popup below the combo box
        pos = self.mapToGlobal(self.rect().bottomLeft())
        self.popup_widget.move(pos)

        # Set width to match combo box
        self.popup_widget.setFixedWidth(self.width())

        # Calculate height based on items + close button
        item_height = 25
        button_height = 35
        max_items = min(7, len(self.items))  # Show max 7 items
        popup_height = (max_items * item_height) + button_height + 15  # 15 for margins
        self.popup_widget.setFixedHeight(popup_height)

        self.popup_widget.show()
        self.popup_widget.raise_()