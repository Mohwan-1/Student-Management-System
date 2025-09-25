#!/usr/bin/env python3
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.main_window import MainWindow
from src.data_manager import DataManager


def main():
    app = QApplication(sys.argv)

    app.setOrganizationName("StudentManagement")
    app.setApplicationName("Student Management System")
    app.setApplicationVersion("1.0")

    # High DPI settings are automatically handled in Qt6

    data_manager = DataManager()
    main_window = MainWindow(data_manager)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()