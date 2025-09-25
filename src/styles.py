DARK_THEME = """
QMainWindow {
    background-color: #1E1E1E;
    color: #FFFFFF;
}

QWidget {
    background-color: #1E1E1E;
    color: #FFFFFF;
    font-family: "Segoe UI", "San Francisco", "Ubuntu", sans-serif;
    font-size: 14px;
}

QFrame {
    background-color: #2D2D2D;
    border: 1px solid #404040;
    border-radius: 6px;
}

QGroupBox {
    background-color: #2D2D2D;
    border: 2px solid #404040;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
    font-size: 16px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #FFFFFF;
}

QPushButton {
    background-color: #0078D4;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    color: #FFFFFF;
    font-weight: bold;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #106EBE;
}

QPushButton:pressed {
    background-color: #005A9E;
}

QPushButton:disabled {
    background-color: #404040;
    color: #808080;
}

QPushButton#successButton {
    background-color: #107C10;
}

QPushButton#successButton:hover {
    background-color: #0E6F0E;
}

QPushButton#warningButton {
    background-color: #FF8C00;
}

QPushButton#warningButton:hover {
    background-color: #E67E00;
}

QPushButton#dangerButton {
    background-color: #D83B01;
}

QPushButton#dangerButton:hover {
    background-color: #C13401;
}

QLineEdit {
    background-color: #2D2D2D;
    border: 2px solid #404040;
    border-radius: 6px;
    padding: 6px;
    color: #FFFFFF;
    selection-background-color: #0078D4;
}

QLineEdit:focus {
    border-color: #0078D4;
}

QComboBox {
    background-color: #2D2D2D;
    border: 2px solid #404040;
    border-radius: 6px;
    padding: 6px;
    color: #FFFFFF;
    min-height: 20px;
}

QComboBox:hover {
    border-color: #606060;
}

QComboBox:focus {
    border-color: #0078D4;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #FFFFFF;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #333333;
    border: 1px solid #404040;
    color: #FFFFFF;
    selection-background-color: #0078D4;
}

QCheckBox {
    spacing: 5px;
    color: #FFFFFF;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #404040;
    border-radius: 3px;
    background-color: #2D2D2D;
}

QCheckBox::indicator:hover {
    border-color: #606060;
}

QCheckBox::indicator:checked {
    background-color: #0078D4;
    border-color: #0078D4;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iMTAiIHZpZXdCb3g9IjAgMCAxMCAxMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEuNSA1TDQgNy41TDguNSAyLjUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
}

QLabel {
    color: #FFFFFF;
    background-color: transparent;
}

QTextEdit {
    background-color: #2D2D2D;
    border: 2px solid #404040;
    border-radius: 6px;
    padding: 6px;
    color: #FFFFFF;
    selection-background-color: #0078D4;
}

QScrollBar:vertical {
    background-color: #2D2D2D;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #606060;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #707070;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #2D2D2D;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #606060;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #707070;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMenuBar {
    background-color: #2D2D2D;
    color: #FFFFFF;
    border-bottom: 1px solid #404040;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #0078D4;
    border-radius: 4px;
}

QMenu {
    background-color: #333333;
    border: 1px solid #404040;
    color: #FFFFFF;
}

QMenu::item {
    padding: 6px 20px;
}

QMenu::item:selected {
    background-color: #0078D4;
}

QStatusBar {
    background-color: #2D2D2D;
    border-top: 1px solid #404040;
    color: #CCCCCC;
}

QToolTip {
    background-color: #333333;
    border: 1px solid #606060;
    color: #FFFFFF;
    padding: 4px;
    border-radius: 4px;
}

QCalendarWidget {
    background-color: #2D2D2D;
    border: 1px solid #404040;
    border-radius: 6px;
}

QCalendarWidget QTableView {
    background-color: #2D2D2D;
    gridline-color: #404040;
    selection-background-color: #0078D4;
    outline: none;
}

QCalendarWidget QHeaderView::section {
    background-color: #333333;
    color: #FFFFFF;
    padding: 4px;
    border: none;
    font-weight: bold;
}

QCalendarWidget QTableView::item {
    padding: 4px;
    border: none;
}

QCalendarWidget QTableView::item:hover {
    background-color: #404040;
}

QCalendarWidget QTableView::item:selected {
    background-color: #0078D4;
    color: #FFFFFF;
}

QSplitter::handle {
    background-color: #404040;
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

QProgressBar {
    background-color: #2D2D2D;
    border: 2px solid #404040;
    border-radius: 6px;
    text-align: center;
    color: #FFFFFF;
}

QProgressBar::chunk {
    background-color: #0078D4;
    border-radius: 4px;
}
"""