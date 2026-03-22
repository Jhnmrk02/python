import sys
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                             QFrame, QVBoxLayout, QComboBox, QApplication, QDateEdit)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QParallelAnimationGroup, QDate
from PyQt6.QtGui import QCursor

class PersonalInfoWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AgaPay - Personal Information")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("background-color: white;")

        olive = "#B9C26E"
        olive_hover = "#A8B15B"
        olive_pressed = "#8C964B"
        light_gray = "#EEEEEE"
        dark_text = "#3B3456"

        self.main_layout = QVBoxLayout(self)
        self.container = QFrame()
        self.container.setFixedSize(950, 620)
        self.main_layout.addWidget(self.container, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- PROGRESS STEPS ---
        for i in range(4):
            circle = QFrame(self.container)
            circle.setGeometry(30, 150 + (i * 70), 32, 32)
            color = olive if i == 1 else "transparent"
            circle.setStyleSheet(f"background-color: {color}; border: 2px solid {olive}; border-radius: 16px;")
            if i < 3:
                line = QFrame(self.container)
                line.setGeometry(45, 182 + (i * 70), 2, 40)
                line.setStyleSheet(f"background-color: {olive};")

        # --- TITLE (ADJUSTED FONT & SPACING) ---
        # In-adjust ang letter-spacing at line-height para hindi dikit-dikit
        title = QLabel("PERSONAL\nINFORMATION", self.container)
        title.setGeometry(130, 40, 500, 110) 
        title.setStyleSheet("""
            color: #D3D3D3; 
            font-size: 45px; 
            font-weight: 800; 
            line-height: 0.7; 
            letter-spacing: 5px; /* Dinagdagan ang spacing para same sa image */
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # --- VERTICAL SEPARATOR LINE ---
        self.v_line = QFrame(self.container)
        self.v_line.setGeometry(480, 235, 2, 230)
        self.v_line.setStyleSheet(f"background-color: {olive};")

        # --- FORM STYLES (UPDATED DROPDOWN ARROW) ---
        input_style = f"""
            QLineEdit, QComboBox, QDateEdit {{
                background-color: {light_gray}; 
                border: 2px solid {olive}; 
                border-radius: 8px; 
                padding-left: 10px; 
                color: #A0A0A0; /* Hint color */
                font-weight: 500;
            }}
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {{
                color: black;
            }}
            
            /* Custom Dropdown Button Logic */
            QComboBox::drop-down, QDateEdit::drop-down {{
                border: none;
                width: 40px;
            }}
            
            /* Eto yung v-shape na arrow same sa image */
            QComboBox::down-arrow, QDateEdit::down-arrow {{
                image: none;
                border-left: 2px solid {olive};
                border-bottom: 2px solid {olive};
                width: 10px;
                height: 10px;
                margin-top: -5px; /* Positioning para pantay */
                transform: rotate(-45deg); /* Rotate para maging 'V' shape */
            }}
        """
        label_style = f"color: {dark_text}; font-size: 13px; font-weight: bold;"

        # --- LEFT COLUMN: FORM ---
        lbl_dob = QLabel("Date of Birth", self.container)
        lbl_dob.setGeometry(130, 170, 150, 20)
        lbl_dob.setStyleSheet(label_style)
        
        self.dob = QDateEdit(self.container)
        self.dob.setGeometry(130, 195, 180, 40)
        self.dob.setCalendarPopup(True)
        self.dob.setDisplayFormat("MM / dd / yyyy")
        self.dob.setDate(QDate(2026, 1, 1))
        self.dob.setStyleSheet(input_style)
        
        lbl_gender = QLabel("Gender", self.container)
        lbl_gender.setGeometry(325, 170, 100, 20)
        lbl_gender.setStyleSheet(label_style)
        
        gender_base_style = f"""
            QPushButton {{
                background-color: white; 
                border: 2px solid {olive}; 
                color: {olive}; 
                border-radius: 20px; 
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {light_gray}; }}
            QPushButton:checked {{ background-color: {olive}; color: white; border: none; }}
        """
        self.btn_male = QPushButton("Male", self.container)
        self.btn_male.setGeometry(325, 195, 70, 40)
        self.btn_male.setCheckable(True)
        self.btn_male.setChecked(True)
        self.btn_male.setStyleSheet(gender_base_style)
        self.btn_male.clicked.connect(lambda: self.toggle_gender(True))
        
        self.btn_female = QPushButton("Female", self.container)
        self.btn_female.setGeometry(400, 195, 70, 40)
        self.btn_female.setCheckable(True)
        self.btn_female.setStyleSheet(gender_base_style)
        self.btn_female.clicked.connect(lambda: self.toggle_gender(False))

        # Civil Status & Nationality
        lbl_status = QLabel("Civil Status", self.container)
        lbl_status.setGeometry(130, 250, 130, 20)
        lbl_status.setStyleSheet(label_style)
        
        self.status = QComboBox(self.container)
        self.status.setGeometry(130, 275, 135, 40)
        self.status.addItems(["Single", "Married", "Divorced", "Widowed"])
        self.status.setStyleSheet(input_style)

        lbl_nat = QLabel("Nationality", self.container)
        lbl_nat.setGeometry(275, 250, 150, 20)
        lbl_nat.setStyleSheet(label_style)
        
        self.nat = QComboBox(self.container)
        self.nat.setGeometry(275, 275, 195, 40)
        self.nat.addItem("Filipino")
        self.nat.setStyleSheet(input_style)

        # ID Fields
        lbl_id_type = QLabel("Valid Government ID Type", self.container)
        lbl_id_type.setGeometry(130, 330, 325, 20)
        lbl_id_type.setStyleSheet(label_style)
        
        self.id_type = QComboBox(self.container)
        self.id_type.setGeometry(130, 355, 340, 40)
        self.id_type.addItems(["UMID", "Driver's License", "SSS", "Passport"])
        self.id_type.setStyleSheet(input_style)

        lbl_id_num = QLabel("Government ID Number", self.container)
        lbl_id_num.setGeometry(130, 410, 325, 20)
        lbl_id_num.setStyleSheet(label_style)
        
        self.id_num = QLineEdit(self.container)
        self.id_num.setGeometry(130, 435, 340, 40)
        self.id_num.setPlaceholderText("0001 - 001 - 001")
        self.id_num.setStyleSheet(input_style)

        # --- NAVIGATION BUTTONS ---
        self.btn_next = QPushButton("Next  〉", self.container)
        self.btn_next.setGeometry(255, 520, 110, 45) 
        self.btn_next.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_next.setStyleSheet(f"""
            QPushButton {{
                background-color: {olive}; color: white; border-radius: 22px;
                font-weight: bold; font-size: 18px; border: none;
            }}
            QPushButton:hover {{ background-color: {olive_hover}; }}
        """)
        self.btn_next.clicked.connect(lambda: self.animate_pop_in(self.btn_next, self.go_to_financial))

        self.btn_prev = QPushButton("〈", self.container)
        self.btn_prev.setGeometry(195, 520, 45, 45)
        self.btn_prev.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_prev.setStyleSheet(f"""
            QPushButton {{
                background-color: white; color: {olive}; border: 2px solid {olive};
                border-radius: 22px; font-weight: bold; font-size: 20px;
            }}
            QPushButton:hover {{ background-color: {light_gray}; }}
        """)
        self.btn_prev.clicked.connect(self.go_back)

        # --- UPLOADS COLUMN ---
        upload_btn_style = f"""
            QPushButton {{
                background-color: {olive}; color: white; border-radius: 15px; 
                font-size: 10px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {olive_hover}; }}
        """

        def create_upload_section(title_text, y):
            lbl = QLabel(title_text, self.container)
            lbl.setGeometry(505, y, 200, 20)
            lbl.setStyleSheet("font-weight: bold; font-size: 13px; color: #333;")
            
            box = QFrame(self.container)
            box.setGeometry(505, y + 25, 155, 90)
            box.setStyleSheet(f"border: 2px solid #AAA; border-radius: 12px; background: white;")
            
            up_btn = QPushButton("Upload Photo", self.container)
            up_btn.setGeometry(505, y + 120, 95, 30)
            up_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            up_btn.setStyleSheet(upload_btn_style)
            return up_btn

        create_upload_section("Front of ID", 110)
        create_upload_section("Back of ID", 270)
        
        lbl_selfie = QLabel("Take a selfie with ID", self.container)
        lbl_selfie.setGeometry(505, 420, 200, 20)
        lbl_selfie.setStyleSheet("font-weight: bold; font-size: 13px; color: #333;")
        
        btn_selfie = QPushButton("Upload Photo", self.container)
        btn_selfie.setGeometry(505, 445, 95, 30)
        btn_selfie.setStyleSheet(upload_btn_style)

        # --- RIGHT PANEL ---
        self.right_panel = QFrame(self.container)
        self.right_panel.setGeometry(680, 20, 270, 580)
        self.right_panel.setStyleSheet(f"background-color: {olive}; border-radius: 40px;")

        side_label = QLabel("Already have an\naccount?", self.right_panel)
        side_label.setGeometry(20, 100, 230, 80)
        side_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold; background: transparent;")
        side_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        sub_label = QLabel("To keep connected with us\nkindly login your account", self.right_panel)
        sub_label.setGeometry(20, 180, 230, 50)
        sub_label.setStyleSheet("color: white; font-size: 12px; background: transparent;")
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_login = QPushButton("Log in", self.right_panel)
        self.btn_login.setGeometry(45, 300, 180, 50)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: transparent; border: 2px solid white; color: white; 
                border-radius: 25px; font-size: 22px; font-weight: bold;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.2); }
        """)
        self.btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_login.clicked.connect(lambda: self.animate_pop_in(self.btn_login, self.go_back))

    def toggle_gender(self, is_male):
        self.btn_male.setChecked(is_male)
        self.btn_female.setChecked(not is_male)

    def animate_pop_in(self, button, callback):
        self.anim_group = QParallelAnimationGroup()
        self.pop_anim = QPropertyAnimation(button, b"geometry")
        self.pop_anim.setDuration(150)
        orig = button.geometry()
        pop_rect = QRect(orig.x() - 5, orig.y() - 5, orig.width() + 10, orig.height() + 10)
        self.pop_anim.setStartValue(orig)
        self.pop_anim.setKeyValueAt(0.5, pop_rect)
        self.pop_anim.setEndValue(orig)
        self.pop_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        self.anim_group.addAnimation(self.pop_anim)
        self.anim_group.finished.connect(callback)
        self.anim_group.start()

    def go_to_financial(self):
        try:
            from financial_info import FinancialForm
            self.financial_screen = FinancialForm(self.main_window)
            self.financial_screen.show()
            self.close()
        except ImportError:
            print("FinancialForm logic not found")

    def go_back(self):
        if self.main_window:
            self.main_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PersonalInfoWindow()
    win.show()
    sys.exit(app.exec())
