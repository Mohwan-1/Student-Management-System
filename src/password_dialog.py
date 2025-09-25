from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor


class PasswordDialog(QDialog):
    def __init__(self, is_new_password=False, parent=None):
        super().__init__(parent)
        self.is_new_password = is_new_password
        self.password = ""
        self.setup_ui()
        self.setModal(True)

    def setup_ui(self):
        self.setWindowTitle("Student Management System")
        self.setFixedSize(400, 200)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("새 비밀번호 설정" if self.is_new_password else "비밀번호 입력")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        description = ("데이터 보안을 위해 비밀번호를 설정해주세요."
                      if self.is_new_password
                      else "기존 데이터에 접근하려면 비밀번호를 입력해주세요.")
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #CCCCCC;")
        layout.addWidget(desc_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("비밀번호를 입력하세요...")
        self.password_input.setMinimumHeight(40)
        self.password_input.returnPressed.connect(self.accept_password)
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_button = QPushButton("취소")
        cancel_button.setMinimumHeight(35)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        confirm_button = QPushButton("확인")
        confirm_button.setMinimumHeight(35)
        confirm_button.setObjectName("successButton")
        confirm_button.clicked.connect(self.accept_password)
        confirm_button.setDefault(True)
        button_layout.addWidget(confirm_button)

        layout.addLayout(button_layout)

        self.password_input.setFocus()

    def accept_password(self):
        password = self.password_input.text().strip()
        if len(password) < 4:
            self.password_input.clear()
            self.password_input.setPlaceholderText("비밀번호는 최소 4자 이상이어야 합니다...")
            self.password_input.setStyleSheet("border-color: #D83B01;")
            return

        self.password = password
        self.accept()

    def get_password(self):
        return self.password