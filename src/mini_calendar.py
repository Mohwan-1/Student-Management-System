from datetime import date, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont


class MiniCalendarCell(QPushButton):
    def __init__(self, cell_date: date):
        super().__init__(str(cell_date.day))
        self.cell_date = cell_date
        # 정사각형으로 크기 조정
        self.setFixedSize(35, 35)

        self.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #404040;
                border-radius: 3px;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton:pressed {
                background-color: #0078D4;
            }
        """)

        if cell_date == date.today():
            self.setStyleSheet("""
                QPushButton {
                    background-color: #0078D4;
                    border: 2px solid #0078D4;
                    border-radius: 3px;
                    color: #FFFFFF;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #106EBE;
                }
            """)

        if cell_date < date.today():
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1A1A1A;
                    border: 1px solid #333333;
                    border-radius: 3px;
                    color: #555555;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1A1A1A;
                    cursor: not-allowed;
                }
            """)
            # 과거 날짜는 비활성화
            self.setEnabled(False)

    def set_selected(self, selected: bool):
        if selected:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #107C10;
                    border: 3px solid #107C10;
                    border-radius: 3px;
                    color: #FFFFFF;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0E6F0E;
                }
            """)
        else:
            if self.cell_date == date.today():
                self.setStyleSheet("""
                    QPushButton {
                        background-color: #0078D4;
                        border: 2px solid #0078D4;
                        border-radius: 3px;
                        color: #FFFFFF;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #106EBE;
                    }
                """)
            elif self.cell_date >= date.today():
                self.setStyleSheet("""
                    QPushButton {
                        background-color: #2D2D2D;
                        border: 1px solid #404040;
                        border-radius: 3px;
                        color: #FFFFFF;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #404040;
                    }
                """)


class MiniCalendar(QWidget):
    dateSelected = Signal(date)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_date = date.today().replace(day=1)
        self.selected_date = None
        self.calendar_cells = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # 헤더
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)

        self.prev_button = QPushButton("◀")
        self.prev_button.setFixedSize(20, 20)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
        """)
        header_layout.addWidget(self.prev_button)

        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #FFFFFF;")
        header_layout.addWidget(self.month_label)

        self.next_button = QPushButton("▶")
        self.next_button.setFixedSize(20, 20)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
        """)
        header_layout.addWidget(self.next_button)

        layout.addLayout(header_layout)

        # 요일 헤더
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        weekday_layout = QHBoxLayout()
        weekday_layout.setSpacing(1)

        for day in weekdays:
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(35, 25)
            label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 10px;
                    color: #CCCCCC;
                    background-color: #333333;
                    border-radius: 3px;
                }
            """)
            weekday_layout.addWidget(label)

        layout.addLayout(weekday_layout)

        # 달력 그리드
        self.calendar_grid = QGridLayout()
        self.calendar_grid.setSpacing(1)

        calendar_frame = QWidget()
        calendar_frame.setLayout(self.calendar_grid)
        layout.addWidget(calendar_frame)

        # 연결
        self.prev_button.clicked.connect(self.prev_month)
        self.next_button.clicked.connect(self.next_month)

        self.update_calendar()

    def update_calendar(self):
        # 기존 셀 제거
        for cell in self.calendar_cells.values():
            self.calendar_grid.removeWidget(cell)
            cell.deleteLater()
        self.calendar_cells.clear()

        # 월 레이블 업데이트
        self.month_label.setText(f"{self.current_date.year}년 {self.current_date.month}월")

        # 달력 생성
        month_start = self.current_date
        month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        # 달력 시작일 (월요일부터 시작)
        calendar_start = month_start - timedelta(days=month_start.weekday())

        current_date = calendar_start
        row = 0

        for week in range(6):  # 최대 6주
            for col in range(7):  # 7일
                cell_date = current_date + timedelta(days=week * 7 + col)

                if cell_date > month_end + timedelta(days=6):
                    break

                cell = MiniCalendarCell(cell_date)

                # 이번 달이 아닌 날짜는 회색으로 (하지만 날짜는 표시)
                if cell_date.month != self.current_date.month:
                    cell.setText(str(cell_date.day))
                    cell.setStyleSheet("""
                        QPushButton {
                            background-color: #1A1A1A;
                            border: 1px solid #333333;
                            border-radius: 3px;
                            color: #666666;
                            font-size: 14px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #2A2A2A;
                        }
                    """)
                    # 다른 달 날짜도 과거면 비활성화
                    if cell_date < date.today():
                        cell.setEnabled(False)

                cell.clicked.connect(lambda checked, d=cell_date: self.on_date_clicked(d))

                self.calendar_cells[cell_date] = cell
                self.calendar_grid.addWidget(cell, week, col)

    def on_date_clicked(self, clicked_date: date):
        if clicked_date.month != self.current_date.month:
            return

        # 과거 날짜 선택 방지
        if clicked_date < date.today():
            return

        # 이미 선택된 날짜를 다시 클릭하면 무시 (중복 선택 방지)
        if self.selected_date == clicked_date:
            return

        # 이전 선택 해제
        if self.selected_date and self.selected_date in self.calendar_cells:
            self.calendar_cells[self.selected_date].set_selected(False)

        # 새로운 선택
        self.selected_date = clicked_date
        self.calendar_cells[clicked_date].set_selected(True)

        self.dateSelected.emit(clicked_date)

    def prev_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()

    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()

    def get_selected_date(self) -> date:
        return self.selected_date

    def set_selected_date(self, selected_date: date):
        # 해당 월로 이동
        if selected_date.month != self.current_date.month or selected_date.year != self.current_date.year:
            self.current_date = selected_date.replace(day=1)
            self.update_calendar()

        # 날짜 선택
        if selected_date in self.calendar_cells:
            if self.selected_date and self.selected_date in self.calendar_cells:
                self.calendar_cells[self.selected_date].set_selected(False)

            self.selected_date = selected_date
            self.calendar_cells[selected_date].set_selected(True)

    def clear_selection(self):
        if self.selected_date and self.selected_date in self.calendar_cells:
            self.calendar_cells[self.selected_date].set_selected(False)
        self.selected_date = None