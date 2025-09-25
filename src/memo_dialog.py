from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class MemoDialog(QDialog):
    def __init__(self, student_name: str, week_number: int, current_memo: str = "", parent=None):
        super().__init__(parent)
        self.student_name = student_name
        self.week_number = week_number
        self.setup_ui()
        self.memo_text.setPlainText(current_memo)

    def setup_ui(self):
        self.setWindowTitle(f"{self.student_name} - {self.week_number}강 메모")
        self.setMinimumSize(400, 300)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 제목
        title_label = QLabel(f"{self.student_name} - {self.week_number}강")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 메모 입력 영역
        memo_label = QLabel("메모:")
        memo_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(memo_label)

        self.memo_text = QTextEdit()
        self.memo_text.setPlaceholderText("이 수업에 대한 메모를 입력하세요...")
        self.memo_text.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-size: 11px;
                color: #FFFFFF;
            }
            QTextEdit:focus {
                border: 2px solid #0078D4;
            }
        """)
        layout.addWidget(self.memo_text)

        # 버튼
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.clear_button = QPushButton("지우기")
        self.clear_button.setMinimumHeight(35)
        self.clear_button.clicked.connect(self.clear_memo)
        button_layout.addWidget(self.clear_button)

        button_layout.addStretch()

        self.cancel_button = QPushButton("취소")
        self.cancel_button.setMinimumHeight(35)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.save_button = QPushButton("저장")
        self.save_button.setMinimumHeight(35)
        self.save_button.setDefault(True)
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

    def clear_memo(self):
        reply = QMessageBox.question(
            self, "메모 삭제 확인",
            "메모를 모두 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.memo_text.clear()

    def get_memo(self) -> str:
        return self.memo_text.toPlainText().strip()

    def has_memo(self) -> bool:
        return bool(self.get_memo())