import random
from datetime import date
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QSpacerItem,
    QSizePolicy, QFrame, QScrollArea
)
from PySide6.QtCore import Signal, Qt

from .data_manager import DataManager
from .models import Student
from .multi_select_combo import MultiSelectComboBox
from .mini_calendar import MiniCalendar


class StudentForm(QWidget):
    studentAdded = Signal(str)
    studentUpdated = Signal(str)

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.current_student = None
        self.is_edit_mode = False
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        form_group = QGroupBox("수강생 등록")
        form_layout = QVBoxLayout(form_group)
        form_layout.setSpacing(12)

        self.name_label = QLabel("수강생 이름 *")
        form_layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("수강생 이름을 입력하세요...")
        self.name_input.setMinimumHeight(35)
        form_layout.addWidget(self.name_input)

        self.course_label = QLabel("총 교육과정 *")
        form_layout.addWidget(self.course_label)

        self.course_combo = QComboBox()
        self.course_combo.setMinimumHeight(35)
        for i in range(1, 11):
            self.course_combo.addItem(f"{i}주차", i)
        form_layout.addWidget(self.course_combo)

        self.weekdays_label = QLabel("수강 요일 *")
        form_layout.addWidget(self.weekdays_label)

        self.weekdays_combo = MultiSelectComboBox()
        weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        self.weekdays_combo.add_items(weekdays)
        form_layout.addWidget(self.weekdays_combo)

        self.start_date_label = QLabel("수강 시작일 *")
        form_layout.addWidget(self.start_date_label)

        self.mini_calendar = MiniCalendar()
        self.mini_calendar.setFixedHeight(220)  # 고정 높이로 변경
        self.mini_calendar.setMinimumWidth(280)  # 최소 너비 설정
        form_layout.addWidget(self.mini_calendar)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.register_button = QPushButton("등록")
        self.register_button.setMinimumHeight(40)
        self.register_button.setObjectName("successButton")
        button_layout.addWidget(self.register_button)

        self.reset_button = QPushButton("초기화")
        self.reset_button.setMinimumHeight(40)
        button_layout.addWidget(self.reset_button)

        self.edit_button = QPushButton("수정")
        self.edit_button.setMinimumHeight(40)
        self.edit_button.setObjectName("warningButton")
        self.edit_button.setVisible(False)
        button_layout.addWidget(self.edit_button)

        self.cancel_button = QPushButton("취소")
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setVisible(False)
        button_layout.addWidget(self.cancel_button)

        form_layout.addLayout(button_layout)
        layout.addWidget(form_group)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        students_group = QGroupBox("등록된 수강생")
        students_layout = QVBoxLayout(students_group)

        self.students_label = QLabel("등록된 수강생이 없습니다.")
        self.students_label.setWordWrap(True)
        self.students_label.setStyleSheet("color: #CCCCCC; padding: 10px;")
        students_layout.addWidget(self.students_label)

        # 수강생 목록을 스크롤 가능하게 설정
        scroll_area = QScrollArea()
        scroll_area.setWidget(students_group)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(200)  # 최소 높이 설정
        scroll_area.setMaximumHeight(300)  # 최대 높이 제한으로 미니 달력 공간 확보

        # 스크롤 영역 스타일 설정
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2D2D2D;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #606060;
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #707070;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        layout.addWidget(scroll_area)

    def setup_connections(self):
        self.register_button.clicked.connect(self.register_student)
        self.reset_button.clicked.connect(self.reset_form)
        self.edit_button.clicked.connect(self.update_student)
        self.cancel_button.clicked.connect(self.cancel_edit)
        self.name_input.returnPressed.connect(self.register_student)

    def register_student(self):
        if not self.validate_input():
            return

        name = self.name_input.text().strip()
        total_weeks = self.course_combo.currentData()
        weekdays = self.weekdays_combo.get_selected_items()
        start_date = self.mini_calendar.get_selected_date() or date.today()

        student = Student(
            name=name,
            total_weeks=total_weeks,
            weekdays=weekdays,
            start_date=start_date,
            color=self.generate_unique_color()
        )

        if self.data_manager.add_student(student):
            self.studentAdded.emit(name)
            self.reset_form()
            self.refresh_students_list()
        else:
            QMessageBox.warning(self, "오류", "수강생 등록에 실패했습니다.")

    def update_student(self):
        if not self.current_student or not self.validate_input():
            return

        name = self.name_input.text().strip()
        total_weeks = self.course_combo.currentData()
        weekdays = self.weekdays_combo.get_selected_items()
        start_date = self.mini_calendar.get_selected_date() or date.today()

        self.current_student.name = name
        self.current_student.total_weeks = total_weeks
        self.current_student.weekdays = weekdays
        self.current_student.start_date = start_date

        if self.data_manager.update_student(self.current_student):
            self.studentUpdated.emit(name)
            self.cancel_edit()
            self.refresh_students_list()
        else:
            QMessageBox.warning(self, "오류", "수강생 정보 수정에 실패했습니다.")

    def validate_input(self) -> bool:
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "입력 오류", "수강생 이름을 입력해주세요.")
            self.name_input.setFocus()
            return False

        if len(name) > 30:
            QMessageBox.warning(self, "입력 오류", "수강생 이름은 30자 이내로 입력해주세요.")
            self.name_input.setFocus()
            return False

        weekdays = self.weekdays_combo.get_selected_items()
        if not weekdays:
            QMessageBox.warning(self, "입력 오류", "최소 1개 이상의 수강 요일을 선택해주세요.")
            return False

        start_date = self.mini_calendar.get_selected_date()
        if not start_date:
            QMessageBox.warning(self, "입력 오류", "수강 시작일을 선택해주세요.")
            return False

        # 수강생 최초 등록 시에만 오늘 이후 날짜로 제한
        if not self.is_edit_mode and start_date < date.today():
            QMessageBox.warning(
                self, "입력 오류",
                "신규 수강생 등록 시 시작일은 오늘 이후여야 합니다.\n"
                "과거 날짜는 수정 모드에서만 설정 가능합니다."
            )
            return False

        return True

    def reset_form(self):
        self.name_input.clear()
        self.course_combo.setCurrentIndex(0)
        self.weekdays_combo.clear_selection()
        self.mini_calendar.clear_selection()
        self.name_input.setFocus()

    def cancel_edit(self):
        self.is_edit_mode = False
        self.current_student = None
        self.reset_form()

        self.register_button.setVisible(True)
        self.reset_button.setVisible(True)
        self.edit_button.setVisible(False)
        self.cancel_button.setVisible(False)

    def edit_student(self, student: Student):
        self.is_edit_mode = True
        self.current_student = student

        self.name_input.setText(student.name)

        for i in range(self.course_combo.count()):
            if self.course_combo.itemData(i) == student.total_weeks:
                self.course_combo.setCurrentIndex(i)
                break

        self.weekdays_combo.set_selected_items(student.weekdays)
        self.mini_calendar.set_selected_date(student.start_date)

        self.register_button.setVisible(False)
        self.reset_button.setVisible(False)
        self.edit_button.setVisible(True)
        self.cancel_button.setVisible(True)

        self.name_input.setFocus()

    def generate_unique_color(self) -> str:
        """기존 수강생들과 중복되지 않는 고유 색상 생성"""
        existing_colors = {student.color for student in self.data_manager.get_students()}

        # HSV 기반으로 균등하게 분포된 색상 생성
        import colorsys

        # 기본 색상 팔레트 (검은 글씨와 대비가 좋은 밝은 색상들)
        base_colors = [
            "#FFB6C1", "#98FB98", "#87CEEB", "#DDA0DD", "#F0E68C",
            "#20B2AA", "#FFA07A", "#90EE90", "#87CEFA", "#B0E0E6",
            "#FFFFE0", "#E0FFFF", "#FFE4E1", "#F0FFF0", "#FFF8DC",
            "#AFEEEE", "#FFEFD5", "#FAFAD2", "#FFE4B5", "#F5DEB3",
            "#E6E6FA", "#D8BFD8", "#THISTLE", "#PLUM", "#LAVENDER",
            "#MISTYROSE", "#ANTIQUEWHITE", "#LINEN", "#BEIGE", "#OLDLACE"
        ]

        # 사용되지 않은 기본 색상이 있으면 그것을 사용
        available_colors = [color for color in base_colors if color not in existing_colors]
        if available_colors:
            return random.choice(available_colors)

        # 모든 기본 색상이 사용된 경우, HSV를 이용해 새 색상 생성
        num_existing = len(existing_colors)
        hue = (num_existing * 0.618033988749895) % 1.0  # 황금비를 이용한 균등 분포
        saturation = 0.3 + (num_existing % 3) * 0.2  # 0.3, 0.5, 0.7 순환
        value = 0.8 + (num_existing % 2) * 0.15  # 0.8, 0.95 순환

        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        color = "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )

        # 기존 색상과 너무 비슷한지 확인 (색상 거리 체크)
        min_distance = 50  # RGB 색상 간 최소 거리
        for existing_color in existing_colors:
            if self._color_distance(color, existing_color) < min_distance:
                # 색상이 너무 비슷하면 조금 변경
                hue = (hue + 0.1) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                color = "#{:02x}{:02x}{:02x}".format(
                    int(rgb[0] * 255),
                    int(rgb[1] * 255),
                    int(rgb[2] * 255)
                )
                break

        return color

    def _color_distance(self, color1: str, color2: str) -> float:
        """두 색상 간의 RGB 거리 계산"""
        try:
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            return ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) ** 0.5
        except:
            return 255  # 오류 발생 시 최대 거리 반환

    def refresh_students_list(self):
        students = self.data_manager.get_students()
        if students:
            students_text = []
            for student in students:
                schedules = self.data_manager.get_schedules_for_student(student.id)

                # 오늘 날짜 기준으로 진도 계산
                today = date.today()
                past_schedules = [s for s in schedules if s.scheduled_date <= today]
                completed = sum(1 for s in past_schedules if s.is_completed)
                expected_completed = len(past_schedules)  # 오늘까지 완료되어야 할 수업 수
                total = len(schedules)

                # 진도율 계산 (오늘까지의 수업 기준)
                if expected_completed > 0:
                    progress_rate = round((completed / expected_completed) * 100)
                    progress = f"{completed}/{expected_completed} ({progress_rate}%)"
                else:
                    progress = f"0/{total} (아직 시작 전)"

                weekdays_text = ", ".join(student.weekdays)
                students_text.append(
                    f"• {student.name} ({student.total_weeks}주차)\n"
                    f"  요일: {weekdays_text}\n"
                    f"  진도: {progress}"
                )

            self.students_label.setText("\n\n".join(students_text))
        else:
            self.students_label.setText("등록된 수강생이 없습니다.")

    def refresh(self):
        self.refresh_students_list()
        if self.is_edit_mode:
            self.cancel_edit()