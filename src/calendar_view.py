from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame, QScrollArea, QMessageBox
)
from PySide6.QtCore import Signal, Qt, QMimeData, QPoint
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent, QDrag, QPainter, QColor, QFont

from .data_manager import DataManager
from .models import Schedule, Student


class ScheduleItem(QFrame):
    def __init__(self, schedule: Schedule, student: Student):
        super().__init__()
        self.schedule = schedule
        self.student = student
        self.drag_start_position = QPoint()

        self.setMinimumHeight(30)
        self.setMaximumHeight(30)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {student.color};
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 2px;
                margin: 1px;
            }}
            QFrame:hover {{
                border: 2px solid #FFFFFF;
                background-color: {self._lighten_color(student.color)};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        text = f"{student.name} {schedule.week_number}주차"
        if schedule.is_completed:
            text += " ✓"

        label = QLabel(text)

        # 완료된 일정은 다른 스타일 적용
        if schedule.is_completed:
            label.setStyleSheet("""
                color: #FFFFFF;
                font-weight: bold;
                font-size: 13px;
                background: rgba(16, 124, 16, 0.8);
                border-radius: 2px;
                padding: 1px 3px;
            """)
            # 완료된 일정의 부모 프레임도 스타일 변경
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {self._darken_color(student.color)};
                    border: 1px solid #107C10;
                    border-radius: 4px;
                    padding: 2px;
                    margin: 1px;
                    opacity: 0.7;
                }}
                QFrame:hover {{
                    border: 2px solid #107C10;
                    background-color: {student.color};
                    opacity: 1.0;
                }}
            """)
        else:
            label.setStyleSheet("""
                color: #000000;
                font-weight: bold;
                font-size: 13px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 2px;
                padding: 1px 3px;
            """)
        label.setWordWrap(True)
        layout.addWidget(label)

    def mouseDoubleClickEvent(self, event):
        """더블클릭으로 완료 상태 토글"""
        if event.button() == Qt.LeftButton:
            # 부모 달력 뷰에 완료 토글 요청
            parent_widget = self.parent()
            while parent_widget and not hasattr(parent_widget, 'toggle_schedule_completion'):
                parent_widget = parent_widget.parent()

            if parent_widget:
                parent_widget.toggle_schedule_completion(self.schedule.id)

    def _lighten_color(self, color: str) -> str:
        """색상을 밝게 만들어 호버 효과에 사용"""
        try:
            # #RRGGBB 형식의 색상을 파싱
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            # 각 채널을 20% 밝게 만들기
            r = min(255, int(r * 1.2))
            g = min(255, int(g * 1.2))
            b = min(255, int(b * 1.2))

            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color

    def _darken_color(self, color: str) -> str:
        """색상을 어둡게 만들어 완료된 일정에 사용"""
        try:
            # #RRGGBB 형식의 색상을 파싱
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            # 각 채널을 30% 어둡게 만들기
            r = int(r * 0.7)
            g = int(g * 0.7)
            b = int(b * 0.7)

            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not (event.buttons() & Qt.LeftButton):
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < 10:
            return

        if self.schedule.is_completed:
            return

        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setText(self.schedule.id)
        drag.setMimeData(mimeData)

        drag.exec_(Qt.MoveAction)


class CalendarCell(QFrame):
    scheduleDropped = Signal(str, date)
    scheduleClicked = Signal(str)

    def __init__(self, cell_date: date):
        super().__init__()
        self.cell_date = cell_date
        self.schedule_items = []

        self.setAcceptDrops(True)
        self.setMinimumHeight(100)
        self.setMinimumWidth(140)

        self.setStyleSheet("""
            QFrame {
                border: 1px solid #404040;
                background-color: #2D2D2D;
            }
            QFrame:hover {
                background-color: #333333;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(1)

        self.date_label = QLabel(str(cell_date.day))
        self.date_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.date_label.setStyleSheet("font-weight: bold; color: #FFFFFF; margin: 2px;")

        if cell_date == date.today():
            self.date_label.setStyleSheet("font-weight: bold; color: #0078D4; margin: 2px;")
            self.setStyleSheet("""
                QFrame {
                    border: 2px solid #0078D4;
                    background-color: #2D2D2D;
                }
                QFrame:hover {
                    background-color: #333333;
                }
            """)

        self.layout.addWidget(self.date_label)
        self.layout.addStretch()

    def add_schedule(self, schedule: Schedule, student: Student):
        item = ScheduleItem(schedule, student)
        self.schedule_items.append(item)
        self.layout.insertWidget(self.layout.count() - 1, item)

    def clear_schedules(self):
        for item in self.schedule_items:
            self.layout.removeWidget(item)
            item.deleteLater()
        self.schedule_items.clear()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            # 모든 날짜로 드래그 가능 (과거 날짜도 허용)
            event.acceptProposedAction()
            if self.cell_date < date.today():
                # 과거 날짜는 주황색으로 표시
                self.setStyleSheet("""
                    QFrame {
                        border: 2px solid #FF8C00;
                        background-color: #333333;
                    }
                """)
            else:
                # 오늘 이후는 초록색으로 표시
                self.setStyleSheet("""
                    QFrame {
                        border: 2px solid #107C10;
                        background-color: #333333;
                    }
                """)

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #404040;
                background-color: #2D2D2D;
            }
            QFrame:hover {
                background-color: #333333;
            }
        """)

    def dropEvent(self, event: QDropEvent):
        schedule_id = event.mimeData().text()
        self.scheduleDropped.emit(schedule_id, self.cell_date)
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #404040;
                background-color: #2D2D2D;
            }
            QFrame:hover {
                background-color: #333333;
            }
        """)
        event.acceptProposedAction()


class CalendarView(QWidget):
    scheduleChanged = Signal(str)

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.current_date = date.today().replace(day=1)
        self.calendar_cells = {}
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        self.prev_button = QPushButton("◀")
        self.prev_button.setFixedSize(40, 30)
        self.prev_button.setToolTip("이전 달")
        header_layout.addWidget(self.prev_button)

        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(self.month_label)

        self.next_button = QPushButton("▶")
        self.next_button.setFixedSize(40, 30)
        self.next_button.setToolTip("다음 달")
        header_layout.addWidget(self.next_button)

        header_layout.addStretch()

        self.today_button = QPushButton("오늘")
        self.today_button.setMinimumWidth(60)
        header_layout.addWidget(self.today_button)

        layout.addLayout(header_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        calendar_widget = QWidget()
        self.calendar_layout = QGridLayout(calendar_widget)
        self.calendar_layout.setSpacing(1)

        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        for i, day in enumerate(weekdays):
            header_label = QLabel(day)
            header_label.setAlignment(Qt.AlignCenter)
            header_label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 14px;
                    background-color: #333333;
                    border: 1px solid #404040;
                    padding: 8px;
                }
            """)
            self.calendar_layout.addWidget(header_label, 0, i)

        scroll_area.setWidget(calendar_widget)
        layout.addWidget(scroll_area)

        self.update_calendar()

    def setup_connections(self):
        self.prev_button.clicked.connect(self.prev_month)
        self.next_button.clicked.connect(self.next_month)
        self.today_button.clicked.connect(self.go_to_today)

    def update_calendar(self):
        self.month_label.setText(f"{self.current_date.year}년 {self.current_date.month}월")

        for cell in self.calendar_cells.values():
            self.calendar_layout.removeWidget(cell)
            cell.deleteLater()
        self.calendar_cells.clear()

        month_start = self.current_date
        month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        calendar_start = month_start - timedelta(days=month_start.weekday())
        calendar_end = month_end + timedelta(days=6 - month_end.weekday())

        current_date = calendar_start
        row = 1

        while current_date <= calendar_end:
            for col in range(7):
                cell_date = current_date + timedelta(days=col)
                cell = CalendarCell(cell_date)
                cell.scheduleDropped.connect(self.on_schedule_dropped)

                if cell_date.month != self.current_date.month:
                    cell.date_label.setStyleSheet("color: #666666; margin: 2px;")

                self.calendar_cells[cell_date] = cell
                self.calendar_layout.addWidget(cell, row, col)

            current_date += timedelta(days=7)
            row += 1

        self.load_schedules()

    def load_schedules(self):
        for cell in self.calendar_cells.values():
            cell.clear_schedules()

        schedules = self.data_manager.get_schedules()
        students_dict = {s.id: s for s in self.data_manager.get_students()}

        for schedule in schedules:
            if schedule.scheduled_date in self.calendar_cells:
                student = students_dict.get(schedule.student_id)
                if student:
                    cell = self.calendar_cells[schedule.scheduled_date]
                    cell.add_schedule(schedule, student)

    def on_schedule_dropped(self, schedule_id: str, new_date: date):
        # 과거 날짜로 이동하는 경우 추가 확인
        if new_date < date.today():
            reply = QMessageBox.question(
                self, "과거 날짜로 일정 이동",
                f"선택한 일정을 과거 날짜({new_date.strftime('%Y년 %m월 %d일')})로 이동하시겠습니까?\n\n"
                "⚠️ 과거 날짜로 이동하는 경우:\n"
                "• 이후 일정들도 자동으로 조정됩니다\n"
                "• 이미 진행된 수업을 기록하는 용도로 사용하세요\n\n"
                "계속하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
        else:
            reply = QMessageBox.question(
                self, "일정 이동 확인",
                f"선택한 일정을 {new_date.strftime('%Y년 %m월 %d일')}로 이동하시겠습니까?\n"
                "이후 일정들도 자동으로 조정됩니다.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

        if reply == QMessageBox.Yes:
            if self.data_manager.move_schedule(schedule_id, new_date):
                if new_date < date.today():
                    self.scheduleChanged.emit("일정이 과거 날짜로 이동되었습니다.")
                else:
                    self.scheduleChanged.emit("일정이 성공적으로 이동되었습니다.")
                self.load_schedules()
            else:
                QMessageBox.warning(self, "오류", "일정 이동에 실패했습니다.")

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

    def go_to_today(self):
        today = date.today()
        self.current_date = today.replace(day=1)
        self.update_calendar()

    def toggle_schedule_completion(self, schedule_id: str):
        """일정의 완료 상태를 토글"""
        schedule = None
        for s in self.data_manager.get_schedules():
            if s.id == schedule_id:
                schedule = s
                break

        if schedule:
            new_status = not schedule.is_completed
            if self.data_manager.mark_schedule_completed(schedule_id, new_status):
                status_text = "완료" if new_status else "미완료"
                self.scheduleChanged.emit(f"'{schedule.week_number}주차' 일정이 {status_text}로 변경되었습니다.")
                self.load_schedules()

    def refresh(self):
        self.load_schedules()