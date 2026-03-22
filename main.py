import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from register_ui import RegistrationWindow 

class AgaPayLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("AgaPay Login")
        self.setFixedSize(900, 500)
        self.setStyleSheet("background-color: white;")

        # --- LEFT PANEL (Olive Section) ---
        self.left_panel = QFrame(self)
        self.left_panel.setGeometry(-20, 20, 300, 460)
        self.left_panel.setStyleSheet("QFrame { background-color: #B9C26E; border-radius: 40px; }")

        signup_label = QLabel("Don't have an\naccount?", self.left_panel)
        signup_label.setGeometry(50, 100, 220, 80)
        signup_label.setStyleSheet("color: white; font-size: 26px; font-weight: bold; background: transparent;")
        signup_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc_label = QLabel("Enter your personal details and\nloan now!", self.left_panel)
        desc_label.setGeometry(50, 180, 220, 60)
        desc_label.setStyleSheet("color: white; font-size: 13px; background: transparent;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_signup = QPushButton("Sign Up", self.left_panel)
        self.btn_signup.setGeometry(75, 260, 150, 45)
        self.btn_signup.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_signup.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid white; color: white; border-radius: 20px; font-size: 18px; font-weight: bold; } QPushButton:hover { background-color: rgba(255, 255, 255, 30); }")
        
        self.btn_signup.clicked.connect(self.open_signup)

        # --- REST OF YOUR UI ---
        logo = QLabel("AgaPay", self)
        logo.setGeometry(450, 60, 400, 100)
        logo.setStyleSheet("color: #B9C26E; font-size: 85px; font-weight: bold;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_email = QLabel("Email / Phone", self)
        lbl_email.setGeometry(460, 190, 200, 30)
        lbl_email.setStyleSheet("color: #3B3456; font-size: 16px; font-weight: bold;")

        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(460, 220, 380, 45)
        self.email_input.setPlaceholderText("Juandelacruz123@gmail.com")
        self.email_input.setStyleSheet("QLineEdit { background-color: #EBEBEB; border: 2px solid #B9C26E; border-radius: 8px; padding-left: 10px; color: #555; }")

        lbl_pass = QLabel("Password", self)
        lbl_pass.setGeometry(460, 280, 200, 30)
        lbl_pass.setStyleSheet("color: #3B3456; font-size: 16px; font-weight: bold;")

        self.pass_input = QLineEdit(self)
        self.pass_input.setGeometry(460, 310, 380, 45)
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setPlaceholderText("********************")
        self.pass_input.setStyleSheet("background-color: #EBEBEB; border: 2px solid #B9C26E; border-radius: 8px; padding-left: 10px;")

        self.btn_login = QPushButton("Login", self)
        self.btn_login.setGeometry(560, 410, 180, 50)
        self.btn_login.setStyleSheet("QPushButton { background-color: #B9C26E; color: white; border-radius: 25px; font-size: 20px; font-weight: bold; } QPushButton:hover { background-color: #A8B25E; }")

    def open_signup(self):
        self.reg_window = RegistrationWindow(self)
        self.reg_window.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgaPayLogin()
    window.show()
    sys.exit(app.exec())
