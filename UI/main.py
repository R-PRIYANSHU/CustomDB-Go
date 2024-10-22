import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLineEdit, QLabel, QStatusBar, QFormLayout)
from PyQt5.QtCore import Qt

class KVStoreGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.kv_store = {}  # Initialize a dictionary for key-value pairs
        self.init_ui()

    def init_ui(self):
        # Set the window title and size
        self.setWindowTitle("Key-Value Store GUI - Step 3")
        self.setGeometry(100, 100, 500, 400)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Dark mode toggle button
        self.dark_mode_button = QPushButton("Toggle Dark Mode")
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        main_layout.addWidget(self.dark_mode_button)

        # Form layout for the key and value input
        form_layout = QFormLayout()
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter key here...")
        form_layout.addRow(QLabel("Enter Key:"), self.key_input)

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Enter value here...")
        form_layout.addRow(QLabel("Enter Value:"), self.value_input)

        main_layout.addLayout(form_layout)

        # Enter button to simulate key submission
        self.enter_button = QPushButton("Enter Key-Value Pair")
        self.enter_button.clicked.connect(self.enter_key_value)
        main_layout.addWidget(self.enter_button)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Apply initial style
        self.apply_style()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_style()

    def apply_style(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2E3440;
                    color: #ECEFF4;
                }
                QPushButton {
                    background-color: #5E81AC;
                    color: #ECEFF4;
                    border: none;
                    padding: 5px 15px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #81A1C1;
                }
                QLineEdit {
                    background-color: #3B4252;
                    color: #ECEFF4;
                    border: 1px solid #4C566A;
                    border-radius: 4px;
                    padding: 5px;
                }
                QStatusBar {
                    background-color: #4C566A;
                    color: #ECEFF4;
                }
            """)
            self.status_bar.showMessage("Dark mode enabled")
        else:
            self.setStyleSheet("")  # Reset to default style
            self.status_bar.showMessage("Dark mode disabled")

    def enter_key_value(self):
        key = self.key_input.text()
        value = self.value_input.text()
        if key and value:
            self.kv_store[key] = value  # Store the key-value pair
            self.status_bar.showMessage(f"Key '{key}' with value '{value}' entered", 3000)
        elif not key:
            self.status_bar.showMessage("No key entered!", 3000)
        elif not value:
            self.status_bar.showMessage("No value entered!", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KVStoreGUI()
    window.show()
    sys.exit(app.exec_())
