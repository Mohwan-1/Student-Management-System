DARK_THEME = """
QMainWindow {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #0F0F23, stop: 1 #161629);
    color: #E4E4E7;
}

QWidget {
    background-color: transparent;
    color: #E4E4E7;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", system-ui, sans-serif;
    font-size: 14px;
    font-weight: 400;
    letter-spacing: 0.01em;
}

QFrame {
    background: rgba(39, 39, 42, 0.6);
    border: 1px solid rgba(63, 63, 70, 0.4);
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

QGroupBox {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(39, 39, 42, 0.8), stop: 1 rgba(24, 24, 27, 0.9));
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 16px;
    margin-top: 16px;
    padding-top: 20px;
    font-weight: 600;
    font-size: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 20px;
    padding: 4px 12px;
    color: #C084FC;
    background: rgba(139, 92, 246, 0.1);
    border-radius: 8px;
    font-weight: 600;
}

QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #8B5CF6, stop: 1 #7C3AED);
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    color: #FFFFFF;
    font-weight: 600;
    font-size: 14px;
    min-height: 20px;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
}

QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #A855F7, stop: 1 #8B5CF6);
    box-shadow: 0 4px 16px rgba(139, 92, 246, 0.4);
    transform: translateY(-1px);
}

QPushButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #7C3AED, stop: 1 #6D28D9);
    box-shadow: 0 1px 4px rgba(139, 92, 246, 0.5);
    transform: translateY(0px);
}

QPushButton:disabled {
    background: rgba(64, 64, 68, 0.6);
    color: rgba(161, 161, 170, 0.7);
    box-shadow: none;
}

QPushButton#successButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #10B981, stop: 1 #059669);
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

QPushButton#successButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #34D399, stop: 1 #10B981);
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
}

QPushButton#warningButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #F59E0B, stop: 1 #D97706);
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

QPushButton#warningButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FCD34D, stop: 1 #F59E0B);
    box-shadow: 0 4px 16px rgba(245, 158, 11, 0.4);
}

QPushButton#dangerButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #EF4444, stop: 1 #DC2626);
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

QPushButton#dangerButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #F87171, stop: 1 #EF4444);
    box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4);
}

QLineEdit {
    background: rgba(39, 39, 42, 0.7);
    border: 2px solid rgba(63, 63, 70, 0.5);
    border-radius: 12px;
    padding: 12px 16px;
    color: #F4F4F5;
    font-size: 14px;
    font-weight: 500;
    selection-background-color: rgba(139, 92, 246, 0.6);
}

QLineEdit:focus {
    border-color: #8B5CF6;
    background: rgba(39, 39, 42, 0.9);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

QComboBox {
    background: rgba(39, 39, 42, 0.7);
    border: 2px solid rgba(63, 63, 70, 0.5);
    border-radius: 12px;
    padding: 12px 16px;
    color: #F4F4F5;
    font-size: 14px;
    font-weight: 500;
    min-height: 20px;
}

QComboBox:hover {
    border-color: rgba(139, 92, 246, 0.6);
    background: rgba(39, 39, 42, 0.8);
}

QComboBox:focus {
    border-color: #8B5CF6;
    background: rgba(39, 39, 42, 0.9);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

QComboBox::drop-down {
    border: none;
    width: 40px;
    background: rgba(139, 92, 246, 0.1);
    border-radius: 8px;
    margin: 2px;
}

QComboBox::drop-down:hover {
    background: rgba(139, 92, 246, 0.2);
}

QComboBox::down-arrow {
    image: none;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-top: 8px solid #A855F7;
    margin-right: 10px;
    width: 0;
    height: 0;
}

QComboBox::down-arrow:hover {
    border-top: 8px solid #C084FC;
}

QComboBox QAbstractItemView {
    background: rgba(24, 24, 27, 0.95);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 12px;
    color: #F4F4F5;
    selection-background-color: rgba(139, 92, 246, 0.6);
    padding: 4px;
}

QCheckBox {
    spacing: 8px;
    color: #F4F4F5;
    font-weight: 500;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(63, 63, 70, 0.6);
    border-radius: 6px;
    background: rgba(39, 39, 42, 0.7);
}

QCheckBox::indicator:hover {
    border-color: rgba(139, 92, 246, 0.6);
    background: rgba(39, 39, 42, 0.8);
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #8B5CF6, stop: 1 #7C3AED);
    border-color: #8B5CF6;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTIgNkw1IDlMMTAgMyIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+Cg==);
}

QLabel {
    color: #F4F4F5;
    background-color: transparent;
    font-weight: 500;
    line-height: 1.4;
}

QTextEdit {
    background: rgba(39, 39, 42, 0.7);
    border: 2px solid rgba(63, 63, 70, 0.5);
    border-radius: 12px;
    padding: 12px 16px;
    color: #F4F4F5;
    font-size: 14px;
    font-weight: 500;
    line-height: 1.5;
    selection-background-color: rgba(139, 92, 246, 0.6);
}

QScrollBar:vertical {
    background: rgba(39, 39, 42, 0.3);
    width: 8px;
    border-radius: 4px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: rgba(139, 92, 246, 0.6);
    border-radius: 4px;
    min-height: 24px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(139, 92, 246, 0.8);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: rgba(39, 39, 42, 0.3);
    height: 8px;
    border-radius: 4px;
    margin: 2px;
}

QScrollBar::handle:horizontal {
    background: rgba(139, 92, 246, 0.6);
    border-radius: 4px;
    min-width: 24px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background: rgba(139, 92, 246, 0.8);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMenuBar {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(39, 39, 42, 0.8), stop: 1 rgba(24, 24, 27, 0.9));
    color: #F4F4F5;
    border-bottom: 1px solid rgba(139, 92, 246, 0.2);
    font-weight: 500;
}

QMenuBar::item {
    background-color: transparent;
    padding: 8px 16px;
    border-radius: 8px;
    margin: 4px 2px;
}

QMenuBar::item:selected {
    background: rgba(139, 92, 246, 0.6);
    color: #FFFFFF;
}

QMenu {
    background: rgba(24, 24, 27, 0.95);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 12px;
    color: #F4F4F5;
    padding: 8px;
}

QMenu::item {
    padding: 10px 16px;
    border-radius: 8px;
    margin: 2px;
    font-weight: 500;
}

QMenu::item:selected {
    background: rgba(139, 92, 246, 0.6);
    color: #FFFFFF;
}

QStatusBar {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(39, 39, 42, 0.8), stop: 1 rgba(24, 24, 27, 0.9));
    border-top: 1px solid rgba(139, 92, 246, 0.2);
    color: #A1A1AA;
    font-weight: 500;
    padding: 4px 16px;
}

QToolTip {
    background: rgba(24, 24, 27, 0.95);
    border: 1px solid rgba(139, 92, 246, 0.3);
    color: #F4F4F5;
    padding: 8px 12px;
    border-radius: 8px;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

QCalendarWidget {
    background: rgba(39, 39, 42, 0.7);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 16px;
    padding: 8px;
}

QCalendarWidget QTableView {
    background: transparent;
    gridline-color: rgba(63, 63, 70, 0.3);
    selection-background-color: rgba(139, 92, 246, 0.6);
    outline: none;
    border-radius: 12px;
}

QCalendarWidget QHeaderView::section {
    background: rgba(139, 92, 246, 0.1);
    color: #C084FC;
    padding: 8px;
    border: none;
    font-weight: 600;
    border-radius: 6px;
    margin: 2px;
}

QCalendarWidget QTableView::item {
    padding: 8px;
    border: none;
    border-radius: 6px;
    margin: 1px;
}

QCalendarWidget QTableView::item:hover {
    background: rgba(139, 92, 246, 0.2);
}

QCalendarWidget QTableView::item:selected {
    background: rgba(139, 92, 246, 0.6);
    color: #FFFFFF;
    font-weight: 600;
}

QSplitter::handle {
    background: rgba(139, 92, 246, 0.3);
    border-radius: 2px;
}

QSplitter::handle:horizontal {
    width: 3px;
    margin: 4px 0;
}

QSplitter::handle:vertical {
    height: 3px;
    margin: 0 4px;
}

QSplitter::handle:hover {
    background: rgba(139, 92, 246, 0.5);
}

QProgressBar {
    background: rgba(39, 39, 42, 0.7);
    border: 2px solid rgba(63, 63, 70, 0.5);
    border-radius: 12px;
    text-align: center;
    color: #F4F4F5;
    font-weight: 600;
    min-height: 8px;
}

QProgressBar::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #8B5CF6, stop: 1 #A855F7);
    border-radius: 10px;
    margin: 1px;
}

QPushButton#navigationArrow {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #8B5CF6, stop: 1 #7C3AED);
    border: none;
    border-radius: 20px;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 18px;
    min-width: 48px;
    max-width: 48px;
    min-height: 40px;
    max-height: 40px;
    padding: 0px;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
}

QPushButton#navigationArrow:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #A855F7, stop: 1 #8B5CF6);
    box-shadow: 0 4px 16px rgba(139, 92, 246, 0.4);
    transform: translateY(-1px);
}

QPushButton#navigationArrow:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #7C3AED, stop: 1 #6D28D9);
    box-shadow: 0 1px 4px rgba(139, 92, 246, 0.5);
    transform: translateY(1px);
}
"""