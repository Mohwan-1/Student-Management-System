from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QStatusBar, QMenuBar, QMenu, QMessageBox, QApplication, QDialog
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence

from .styles import DARK_THEME
from .data_manager import DataManager
from .password_dialog import PasswordDialog
from .student_form import StudentForm
from .calendar_view import CalendarView
from .student_manager_dialog import StudentManagerDialog


class MainWindow(QMainWindow):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.setup_ui()
        self.setup_menu()
        self.setup_connections()
        self.authenticate()

    def setup_ui(self):
        self.setWindowTitle("Student Management System v1.0")
        self.setMinimumSize(1200, 800)
        self.resize(1600, 900)

        self.setStyleSheet(DARK_THEME)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        splitter = QSplitter(Qt.Horizontal)

        self.student_form = StudentForm(self.data_manager)
        self.student_form.setMinimumWidth(320)
        self.student_form.setMaximumWidth(380)

        self.calendar_view = CalendarView(self.data_manager)

        splitter.addWidget(self.student_form)
        splitter.addWidget(self.calendar_view)
        splitter.setSizes([320, 1000])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        main_layout.addWidget(splitter)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("준비 완료")

    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("파일(&F)")

        new_action = QAction("새 데이터베이스", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_database)
        file_menu.addAction(new_action)

        file_menu.addSeparator()

        backup_action = QAction("백업 생성", self)
        backup_action.setShortcut("Ctrl+B")
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)

        file_menu.addSeparator()

        exit_action = QAction("종료", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 수강생 메뉴 추가
        student_menu = menubar.addMenu("수강생(&S)")

        manage_students_action = QAction("수강생 관리", self)
        manage_students_action.setShortcut("Ctrl+M")
        manage_students_action.triggered.connect(self.show_student_manager)
        student_menu.addAction(manage_students_action)

        student_menu.addSeparator()

        update_colors_action = QAction("수강생 색상 업데이트", self)
        update_colors_action.triggered.connect(self.update_student_colors)
        student_menu.addAction(update_colors_action)

        edit_menu = menubar.addMenu("편집(&E)")

        undo_action = QAction("실행 취소", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.undo_last_action)
        edit_menu.addAction(undo_action)

        help_menu = menubar.addMenu("도움말(&H)")

        about_action = QAction("정보", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_connections(self):
        self.data_manager.dataChanged.connect(self.on_data_changed)
        self.student_form.studentAdded.connect(self.on_student_added)
        self.calendar_view.scheduleChanged.connect(self.on_schedule_changed)

    def authenticate(self):
        if self.data_manager.has_existing_data():
            dialog = PasswordDialog(is_new_password=False, parent=self)
            if dialog.exec() == QDialog.Accepted:
                password = dialog.get_password()
                if self.data_manager.load_data(password):
                    self.status_bar.showMessage("데이터를 성공적으로 불러왔습니다.")
                    self.refresh_views()
                else:
                    QMessageBox.critical(self, "오류", "비밀번호가 올바르지 않거나 데이터 파일이 손상되었습니다.")
                    QApplication.quit()
            else:
                QApplication.quit()
        else:
            dialog = PasswordDialog(is_new_password=True, parent=self)
            if dialog.exec() == QDialog.Accepted:
                password = dialog.get_password()
                self.data_manager.set_password(password)
                self.data_manager.save_data()
                self.status_bar.showMessage("새 데이터베이스가 생성되었습니다.")
            else:
                QApplication.quit()

    def refresh_views(self):
        self.student_form.refresh()
        self.calendar_view.refresh()

    def on_data_changed(self):
        self.refresh_views()
        self.status_bar.showMessage("데이터가 업데이트되었습니다.", 3000)

    def on_student_added(self, student_name):
        self.status_bar.showMessage(f"수강생 '{student_name}'이(가) 추가되었습니다.", 3000)

    def on_schedule_changed(self, message):
        self.status_bar.showMessage(message, 3000)

    def new_database(self):
        reply = QMessageBox.question(
            self, "새 데이터베이스",
            "현재 데이터가 모두 삭제됩니다. 계속하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            dialog = PasswordDialog(is_new_password=True, parent=self)
            if dialog.exec() == QDialog.Accepted:
                password = dialog.get_password()
                self.data_manager.data.students.clear()
                self.data_manager.data.schedules.clear()
                self.data_manager.set_password(password)
                self.data_manager.save_data()
                self.refresh_views()

    def create_backup(self):
        if self.data_manager.create_backup():
            QMessageBox.information(self, "백업 완료", "백업이 성공적으로 생성되었습니다.")
        else:
            QMessageBox.warning(self, "백업 실패", "백업 생성에 실패했습니다.")

    def show_student_manager(self):
        dialog = StudentManagerDialog(self.data_manager, self)
        dialog.studentDeleted.connect(self.on_student_deleted)
        dialog.studentUpdated.connect(self.refresh_views)
        dialog.exec()

    def on_student_deleted(self, student_name):
        self.status_bar.showMessage(f"수강생 '{student_name}'이(가) 삭제되었습니다.", 3000)

    def update_student_colors(self):
        """기존 수강생들의 색상을 강렬한 색상으로 업데이트"""
        students = self.data_manager.get_students()
        if not students:
            QMessageBox.information(self, "색상 업데이트", "업데이트할 수강생이 없습니다.")
            return

        reply = QMessageBox.question(
            self, "색상 업데이트 확인",
            f"현재 등록된 {len(students)}명 수강생의 색상을 강렬한 고대비 색상으로 업데이트하시겠습니까?\n\n"
            "기존 색상은 모두 새로운 색상으로 변경됩니다.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # 강렬한 기본 색상 팔레트
                vibrant_colors = [
                    "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
                    "#FF6600", "#FF0066", "#66FF00", "#0066FF", "#6600FF", "#FF3300",
                    "#FF3333", "#33FF33", "#3333FF", "#FFFF33", "#FF33FF", "#33FFFF",
                    "#CC0000", "#00CC00", "#0000CC", "#CCCC00", "#CC00CC", "#00CCCC",
                    "#EE4B2B", "#228B22", "#4169E1", "#FF1493", "#FF8C00", "#8A2BE2",
                ]

                updated_count = 0
                for i, student in enumerate(students):
                    if i < len(vibrant_colors):
                        old_color = student.color
                        student.color = vibrant_colors[i]
                        updated_count += 1
                        print(f"수강생 '{student.name}' 색상 업데이트: {old_color} -> {student.color}")

                if self.data_manager.save_data():
                    self.refresh_views()
                    QMessageBox.information(
                        self, "색상 업데이트 완료",
                        f"{updated_count}명 수강생의 색상이 강렬한 색상으로 업데이트되었습니다."
                    )
                    self.status_bar.showMessage(f"{updated_count}명 수강생 색상 업데이트 완료", 3000)
                else:
                    QMessageBox.warning(self, "오류", "색상 업데이트 저장에 실패했습니다.")

            except Exception as e:
                QMessageBox.critical(self, "오류", f"색상 업데이트 중 오류가 발생했습니다: {str(e)}")

    def undo_last_action(self):
        pass

    def show_about(self):
        QMessageBox.about(
            self, "정보",
            "<h3>Student Management System v1.0</h3>"
            "<p>수강생의 교육 일정을 효율적으로 관리하는 프로그램입니다.</p>"
            "<p><b>개발:</b> PySide6, Python 3.8+</p>"
            "<p><b>암호화:</b> AES-256 보안</p>"
            "<p><b>특징:</b> 오프라인 독립 실행, 드래그 앤 드롭 일정 관리</p>"
        )

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "종료 확인",
            "프로그램을 종료하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()