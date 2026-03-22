import sys
import re
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFrame, QCheckBox, QVBoxLayout
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QCursor
from personal_info import PersonalInfoWindow 

class RegistrationWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window 
        self.inputs = {} 
        self.error_labels = {} 
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AgaPay - Registration")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("background-color: white;")

        olive = "#B9C26E"
        olive_hover = "#A8B15B" 
        dark_text = "#3B3456"

        self.main_layout = QVBoxLayout(self)
        self.container = QFrame()
        self.container.setFixedSize(950, 620)
        self.main_layout.addWidget(self.container, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- PROGRESS STEPS ---
        for i in range(4):
            circle = QFrame(self.container)
            circle.setGeometry(30, 150 + (i * 70), 32, 32)
            color = olive if i == 0 else "transparent"
            circle.setStyleSheet(f"background-color: {color}; border: 2px solid {olive}; border-radius: 16px;")
            if i < 3:
                line = QFrame(self.container)
                line.setStyleSheet(f"background-color: {olive};")
                line.setGeometry(45, 182 + (i * 70), 2, 40)

        # --- CENTER: THE FORM TITLE ---
        # Lakihan ang font-size (45px) at width (800) para maging kamukha ng sample images
        title = QLabel("BASIC INFORMATION", self.container)
        title.setGeometry(160, 5, 800, 90) 
        title.setStyleSheet("color: #D3D3D3; font-size: 45px; font-weight: bold; letter-spacing: 1px;")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        def create_input(key, label_text, x, y, w, placeholder, is_pass=False, optional=False):
            lbl = QLabel(label_text, self.container)
            lbl.setGeometry(x, y, w, 20)
            lbl.setStyleSheet(f"color: {dark_text}; font-size: 13px; font-weight: bold;")
            
            entry = QLineEdit(self.container)
            entry.setGeometry(x, y + 22, w, 38)
            entry.setPlaceholderText(placeholder)
            if is_pass: entry.setEchoMode(QLineEdit.EchoMode.Password)
            entry.setStyleSheet(f"background-color: #EEEEEE; border: 2px solid {olive}; border-radius: 6px; padding-left: 10px; color: #333;")
            
            err_lbl = QLabel("This field is required", self.container)
            err_lbl.setGeometry(x, y + 60, w, 15)
            err_lbl.setStyleSheet("color: red; font-size: 10px; font-weight: bold;")
            err_lbl.hide()
            
            self.inputs[key] = {"widget": entry, "optional": optional}
            self.error_labels[key] = err_lbl
            return entry

        # Inputs layout - In-adjust ang Y coordinates para may space sa malaking title
        create_input("fname", "First Name", 160, 95, 150, "e.g. Juan")
        create_input("mname", "Middle Name (Optional)", 320, 95, 150, "e.g. Santos", optional=True)
        create_input("lname", "Last Name", 480, 95, 150, "e.g. Dela Cruz")
        create_input("email", "Email Address", 160, 180, 260, "JuanDelaCruz123@gmail.com")
        create_input("phone", "Phone Number", 435, 180, 195, "09123456789")
        create_input("pass", "Password", 160, 260, 470, "Create a password", True)
        create_input("cpass", "Confirm Password", 160, 340, 470, "Repeat your password", True)
        create_input("user", "Username (Optional)", 160, 420, 470, "e.g. JuanDelaCruz123", optional=True)

        self.cb = QCheckBox("I have read through and fully consent to and agree with the\nTerms and Conditions and Privacy Policy", self.container)
        self.cb.setGeometry(240, 490, 400, 45)
        self.cb.setStyleSheet("font-size: 11px; color: #555; font-weight: bold;")

        # --- NEXT BUTTON ---
        btn_next = QPushButton("Next  〉", self.container)
        btn_next.setGeometry(335, 550, 110, 45) 
        btn_next.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_next.setStyleSheet(f"""
            QPushButton {{
                background-color: {olive};
                color: white;
                border-radius: 22px;
                font-weight: bold;
                font-size: 18px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {olive_hover};
            }}
        """)
        btn_next.clicked.connect(self.validate_and_next)

        # Right Panel Style
        self.right_panel = QFrame(self.container)
        self.right_panel.setGeometry(680, 20, 270, 580)
        self.right_panel.setStyleSheet(f"background-color: {olive}; border-radius: 40px;")

        side_label = QLabel("Already have an\naccount?", self.right_panel)
        side_label.setGeometry(20, 120, 230, 80)
        side_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold; background: transparent;")
        side_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_login_back = QPushButton("Log in", self.right_panel)
        self.btn_login_back.setGeometry(45, 320, 180, 50)
        self.btn_login_back.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid white;
                color: white;
                border-radius: 25px;
                font-size: 22px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.btn_login_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_login_back.clicked.connect(self.go_to_login)

    def validate_and_next(self):
        is_all_valid = True
        name_pattern = r"^[a-zA-Z\s\-']+$"

        for key in ["fname", "lname"]:
            text = self.inputs[key]["widget"].text().strip()
            if text == "":
                self.error_labels[key].setText("This field is required")
                self.error_labels[key].show()
                is_all_valid = False
            elif len(text) < 4:
                self.error_labels[key].setText("Must be at least 4 characters")
                self.error_labels[key].show()
                is_all_valid = False
            elif not re.match(name_pattern, text):
                self.error_labels[key].setText("Numbers/Symbols not allowed")
                self.error_labels[key].show()
                is_all_valid = False
            else:
                self.error_labels[key].hide()

        mname_text = self.inputs["mname"]["widget"].text().strip()
        if mname_text:
            if not re.match(name_pattern, mname_text):
                self.error_labels["mname"].setText("Invalid characters")
                self.error_labels["mname"].show()
                is_all_valid = False
            else:
                self.error_labels["mname"].hide()

        email_text = self.inputs["email"]["widget"].text().strip()
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if email_text == "":
            self.error_labels["email"].setText("This field is required")
            self.error_labels["email"].show()
            is_all_valid = False
        elif not re.match(email_pattern, email_text):
            self.error_labels["email"].setText("Invalid email format")
            self.error_labels["email"].show()
            is_all_valid = False
        else:
            self.error_labels["email"].hide()

        phone_text = self.inputs["phone"]["widget"].text().strip()
        phone_pattern = r'^(09|\+639)\d{9}$'
        if phone_text == "":
            self.error_labels["phone"].setText("This field is required")
            self.error_labels["phone"].show()
            is_all_valid = False
        elif not re.match(phone_pattern, phone_text):
            self.error_labels["phone"].setText("Invalid PH number (11 digits)")
            self.error_labels["phone"].show()
            is_all_valid = False
        else:
            self.error_labels["phone"].hide()

        password = self.inputs["pass"]["widget"].text()
        confirm_password = self.inputs["cpass"]["widget"].text()
        
        if password == "":
            self.error_labels["pass"].setText("This field is required")
            self.error_labels["pass"].show()
            is_all_valid = False
        elif len(password) < 8:
            self.error_labels["pass"].setText("Must be at least 8 characters")
            self.error_labels["pass"].show()
            is_all_valid = False
        else:
            self.error_labels["pass"].hide()

        if confirm_password != password:
            self.error_labels["cpass"].setText("Passwords do not match")
            self.error_labels["cpass"].show()
            is_all_valid = False
        else:
            self.error_labels["cpass"].hide()

        if not self.cb.isChecked():
            is_all_valid = False

        if is_all_valid:
            self.next_screen = PersonalInfoWindow(self)
            self.next_screen.show()
            self.hide() 

    def go_to_login(self):
        if self.main_window:
            self.main_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RegistrationWindow()
    win.show()
    sys.exit(app.exec())
