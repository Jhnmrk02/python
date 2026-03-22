import sys
import re
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                             QFrame, QVBoxLayout, QApplication, QMessageBox)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QParallelAnimationGroup
from PyQt6.QtGui import QCursor

class FinancialForm(QWidget):
    def __init__(self, main_window=None): 
        super().__init__()
        self.main_window = main_window
        self.inputs = {} 
        self.error_labels = {} 
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AgaPay - Financial Information")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("background-color: white;")

        self.olive = "#B9C26E"
        self.olive_hover = "#A8B15B"
        dark_text = "#3B3456"
        light_gray = "#EEEEEE"

        self.main_layout = QVBoxLayout(self)
        self.container = QFrame()
        self.container.setFixedSize(950, 620)
        self.main_layout.addWidget(self.container, alignment=Qt.AlignmentFlag.AlignCenter)

        for i in range(4):
            circle = QFrame(self.container)
            circle.setGeometry(30, 150 + (i * 70), 32, 32)
            color = self.olive if i == 2 else "transparent"
            circle.setStyleSheet(f"background-color: {color}; border: 2px solid {self.olive}; border-radius: 16px;")
            if i < 3:
                line = QFrame(self.container)
                line.setGeometry(45, 182 + (i * 70), 2, 40)
                line.setStyleSheet(f"background-color: {self.olive};")

        title = QLabel("FINANCIAL INFORMATION", self.container)
        title.setGeometry(160, 5, 700, 70) 
        title.setStyleSheet("color: #D3D3D3; font-size: 35px; font-weight: bold;")

        def create_field(key, label_text, x, y, w, placeholder="", optional=False):
            lbl = QLabel(label_text, self.container)
            lbl.setGeometry(x, y, w, 20)
            lbl.setStyleSheet(f"color: {dark_text}; font-size: 13px; font-weight: bold;")
            
            entry = QLineEdit(self.container)
            entry.setGeometry(x, y + 22, w, 35) # Reduced height slightly to save space
            entry.setPlaceholderText(placeholder)
            entry.setStyleSheet(f"background-color: {light_gray}; border: 2px solid {self.olive}; border-radius: 6px; padding-left: 10px; color: black;")
            
            # Adjusted error label position (y + 58) para hindi sumabog sa layout
            err_lbl = QLabel("This field is required", self.container)
            err_lbl.setGeometry(x, y + 58, w, 12)
            err_lbl.setStyleSheet("color: red; font-size: 10px; font-weight: bold;")
            err_lbl.hide()
            
            self.inputs[key] = {"widget": entry, "optional": optional, "type": label_text}
            self.error_labels[key] = err_lbl
            return entry

        # --- ROW 1: BANK INFO (Y=80) ---
        create_field("bank_name", "Bank Name", 160, 80, 140, "e.g. BDO / BPI")
        create_field("bank_acc", "Bank Account Number", 310, 80, 180, "0012 3456 7890")
        create_field("acc_name", "Account Holder Name", 500, 80, 150, "e.g. Juan")

        # --- ROW 2: E-WALLET (Y=165) ---
        sub_title1 = QLabel("GCash / Maya Account (Optional)", self.container)
        sub_title1.setGeometry(160, 165, 300, 20)
        sub_title1.setStyleSheet("color: #D3D3D3; font-weight: bold; font-size: 16px;")

        create_field("wallet_num", "E - Wallet Account Number", 160, 190, 260, "e.g. 09123456789", optional=True)
        create_field("wallet_name", "Account Name", 435, 190, 215, "e.g. Juan Dela Cruz", optional=True)

        # --- ROW 3: EMERGENCY CONTACT TITLE (Y=265) ---
        title2 = QLabel("EMERGENCY CONTACT", self.container)
        title2.setGeometry(160, 265, 470, 40)
        title2.setStyleSheet("color: #D3D3D3; font-size: 35px; font-weight: bold;")

        # --- ROW 4: CONTACT PERSON 1 (Y=310) ---
        sub_title2 = QLabel("Contact Person 1", self.container)
        sub_title2.setGeometry(160, 310, 200, 20)
        sub_title2.setStyleSheet("color: #D3D3D3; font-weight: bold; font-size: 14px;")

        create_field("c1_name", "Contact Name", 160, 335, 180, "Full Name")
        create_field("c1_rel", "Relationship", 350, 335, 130, "e.g. Mother")
        create_field("c1_num", "Contact Number", 490, 335, 160, "09xxxxxxxxx")

        # --- ROW 5: CONTACT PERSON 2 (Y=415) ---
        sub_title3 = QLabel("Contact Person 2", self.container)
        sub_title3.setGeometry(160, 415, 200, 20)
        sub_title3.setStyleSheet("color: #D3D3D3; font-weight: bold; font-size: 14px;")

        create_field("c2_name", "Contact Name", 160, 440, 180, "Full Name")
        create_field("c2_rel", "Relationship", 350, 440, 130, "e.g. Friend")
        create_field("c2_num", "Contact Number", 490, 440, 160, "09xxxxxxxxx")

        # --- NAVIGATION BUTTONS ---
        self.btn_prev = QPushButton("〈", self.container)
        self.btn_prev.setGeometry(275, 545, 45, 45) # Lowered to avoid overlap
        self.btn_prev.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_prev.setStyleSheet(f"QPushButton {{ background-color: white; color: {self.olive}; border: 2px solid {self.olive}; border-radius: 22px; font-weight: bold; font-size: 20px; }} QPushButton:hover {{ background-color: {light_gray}; }}")
        self.btn_prev.clicked.connect(self.go_back_to_personal)

        self.next_button = QPushButton("Finish", self.container)
        self.next_button.setGeometry(335, 545, 110, 45)
        self.next_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.next_button.setStyleSheet(f"QPushButton {{ background-color: {self.olive}; color: white; border-radius: 22px; font-weight: bold; font-size: 18px; border: none; }} QPushButton:hover {{ background-color: {self.olive_hover}; }}")
        self.next_button.clicked.connect(lambda: self.animate_pop_in(self.next_button, self.validate_and_finish))

        # --- RIGHT PANEL ---
        self.right_panel = QFrame(self.container)
        self.right_panel.setGeometry(680, 20, 270, 580)
        self.right_panel.setStyleSheet(f"background-color: {self.olive}; border-radius: 40px;")

        side_label = QLabel("Already have an\naccount?", self.right_panel)
        side_label.setGeometry(20, 120, 230, 80)
        side_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold; background: transparent;")
        side_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_login = QPushButton("Log in", self.right_panel)
        self.btn_login.setGeometry(45, 320, 180, 50)
        self.btn_login.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid white; color: white; border-radius: 25px; font-size: 22px; font-weight: bold; } QPushButton:hover { background-color: rgba(255, 255, 255, 0.2); }")
        self.btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_login.clicked.connect(lambda: self.animate_pop_in(self.btn_login, self.go_back))

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

    def validate_and_finish(self):
        is_all_valid = True
        phone_pattern = r'^(09|\+639)\d{9}$'
        
        for key, data in self.inputs.items():
            text = data["widget"].text().strip()
            optional = data["optional"]
            field_type = data["type"]

            if not optional and text == "":
                self.error_labels[key].setText("This field is required")
                self.error_labels[key].show()
                is_all_valid = False
            elif text and "Number" in field_type:
                clean_phone = text.replace(" ", "")
                if not re.match(phone_pattern, clean_phone):
                    self.error_labels[key].setText("Invalid PH number")
                    self.error_labels[key].show()
                    is_all_valid = False
                else:
                    self.error_labels[key].hide()
            else:
                self.error_labels[key].hide()

        if is_all_valid:
            QMessageBox.information(self, "Success", "Registration Complete!")

    def go_back_to_personal(self):
        try:
            from personal_info import PersonalInfoWindow
            self.personal_window = PersonalInfoWindow(self.main_window)
            self.personal_window.show()
            self.close()
        except ImportError:
            if self.main_window: self.main_window.show()
            self.close()

    def go_back(self):
        if self.main_window: self.main_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FinancialForm()
    win.show()
    sys.exit(app.exec())
