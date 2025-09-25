from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
    QAbstractItemView, QCheckBox, QWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from .data_manager import DataManager
from .models import Student


class StudentManagerDialog(QDialog):
    studentDeleted = Signal(str)  # 학생 삭제 시그널
    studentUpdated = Signal()     # 학생 업데이트 시그널

    def __init__(self, data_manager: DataManager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()
        self.setup_connections()
        self.refresh_students()

    def setup_ui(self):
        self.setWindowTitle("수강생 관리")
        self.setMinimumSize(700, 500)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 제목
        title_label = QLabel("등록된 수강생 관리")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "선택", "이름", "총 과정", "수강 요일", "시작일", "진도", "상태"
        ])

        # 테이블 스타일
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2D2D2D;
                gridline-color: #404040;
                border: 1px solid #404040;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #404040;
            }
            QTableWidget::item:selected {
                background-color: #0078D4;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

        # 테이블 설정
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)

        # 열 크기 자동 조정
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 선택
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 이름
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 총 과정
        header.setSectionResizeMode(3, QHeaderView.Stretch)           # 수강 요일
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 시작일
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # 진도
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # 상태

        layout.addWidget(self.table)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.select_all_button = QPushButton("모두 선택")
        self.select_all_button.setMinimumHeight(35)
        button_layout.addWidget(self.select_all_button)

        self.deselect_all_button = QPushButton("모두 해제")
        self.deselect_all_button.setMinimumHeight(35)
        button_layout.addWidget(self.deselect_all_button)

        button_layout.addStretch()

        self.delete_selected_button = QPushButton("선택된 수강생 삭제")
        self.delete_selected_button.setMinimumHeight(35)
        self.delete_selected_button.setObjectName("dangerButton")
        self.delete_selected_button.setEnabled(False)
        button_layout.addWidget(self.delete_selected_button)

        self.close_button = QPushButton("닫기")
        self.close_button.setMinimumHeight(35)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

    def setup_connections(self):
        self.select_all_button.clicked.connect(self.select_all_students)
        self.deselect_all_button.clicked.connect(self.deselect_all_students)
        self.delete_selected_button.clicked.connect(self.delete_selected_students)
        self.close_button.clicked.connect(self.accept)

    def refresh_students(self):
        students = self.data_manager.get_students()
        self.table.setRowCount(len(students))

        for row, student in enumerate(students):
            # 체크박스
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.setAlignment(Qt.AlignCenter)

            checkbox = QCheckBox()
            checkbox.setObjectName(f"checkbox_{student.id}")
            checkbox.stateChanged.connect(self.on_checkbox_changed)
            checkbox_layout.addWidget(checkbox)

            self.table.setCellWidget(row, 0, checkbox_widget)

            # 이름
            name_item = QTableWidgetItem(student.name)
            name_item.setData(Qt.UserRole, student.id)
            self.table.setItem(row, 1, name_item)

            # 총 과정
            course_item = QTableWidgetItem(f"{student.total_weeks}강")
            self.table.setItem(row, 2, course_item)

            # 수강 요일
            weekdays_text = ", ".join(student.weekdays)
            weekdays_item = QTableWidgetItem(weekdays_text)
            self.table.setItem(row, 3, weekdays_item)

            # 시작일
            start_date_item = QTableWidgetItem(student.start_date.strftime("%Y-%m-%d"))
            self.table.setItem(row, 4, start_date_item)

            # 진도 (오늘 날짜 기준 주차 / 총 주차)
            from datetime import date
            today = date.today()

            if student.start_date <= today:
                # 시작일부터 오늘까지의 경과 일수
                days_passed = (today - student.start_date).days

                # 경과 강수 계산 (1강부터 시작하므로 +1)
                current_week = min(days_passed // 7 + 1, student.total_weeks)

                # 진도율 계산
                if student.total_weeks > 0:
                    progress_percentage = round((current_week / student.total_weeks) * 100)
                    progress_text = f"{current_week}/{student.total_weeks} ({progress_percentage}%)"
                else:
                    progress_text = "0/0 (0%)"
            else:
                # 아직 시작하지 않은 경우
                progress_text = f"0/{student.total_weeks} (시작 예정)"

            progress_item = QTableWidgetItem(progress_text)
            self.table.setItem(row, 5, progress_item)

            # 상태
            status = "활성" if student.is_active else "비활성"
            status_item = QTableWidgetItem(status)
            if student.is_active:
                status_item.setForeground(Qt.green)
            else:
                status_item.setForeground(Qt.red)
            self.table.setItem(row, 6, status_item)

    def on_checkbox_changed(self):
        """체크박스 상태 변경 시 삭제 버튼 활성화/비활성화"""
        selected_students = self.get_selected_students()
        self.delete_selected_button.setEnabled(len(selected_students) > 0)

    def get_selected_students(self):
        """선택된 수강생 ID 목록 반환"""
        selected_students = []
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    name_item = self.table.item(row, 1)  # 이름이 1번 열로 이동
                    if name_item:
                        student_id = name_item.data(Qt.UserRole)
                        selected_students.append(student_id)
        return selected_students

    def select_all_students(self):
        """모든 수강생 선택"""
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(True)

    def deselect_all_students(self):
        """모든 수강생 선택 해제"""
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(False)

    def delete_selected_students(self):
        """선택된 수강생들 삭제"""
        selected_students = self.get_selected_students()
        if not selected_students:
            QMessageBox.warning(self, "선택 오류", "삭제할 수강생을 선택해주세요.")
            return

        # 선택된 수강생 이름들 가져오기
        student_names = []
        for student_id in selected_students:
            student = self.data_manager.get_student_by_id(student_id)
            if student:
                student_names.append(student.name)

        # 삭제 확인
        names_text = ", ".join(student_names)
        reply = QMessageBox.question(
            self, "수강생 삭제 확인",
            f"다음 수강생들을 삭제하시겠습니까?\n\n"
            f"{names_text}\n\n"
            f"관련된 모든 일정도 함께 삭제됩니다.\n"
            f"이 작업은 되돌릴 수 없습니다.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            deleted_count = 0
            for student_id in selected_students:
                if self.data_manager.remove_student(student_id):
                    deleted_count += 1

            if deleted_count > 0:
                self.studentDeleted.emit(f"{deleted_count}명의 수강생")
                self.refresh_students()
                QMessageBox.information(
                    self, "삭제 완료",
                    f"{deleted_count}명의 수강생이 삭제되었습니다."
                )
            else:
                QMessageBox.warning(
                    self, "삭제 실패",
                    "수강생 삭제에 실패했습니다."
                )