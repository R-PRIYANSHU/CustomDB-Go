import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QStatusBar, QFormLayout, QComboBox)
from PyQt5.QtCore import Qt

class KVStoreGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.server_url = "http://localhost:8080"  # URL for server operations
        self.init_ui()

    def init_ui(self):
        # Set the window title and size
        self.setWindowTitle("Key-Value Store GUI - Enhanced")
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

        # Operation selection
        self.op_combo = QComboBox()
        self.op_combo.addItems(["set", "get", "del"])  # Add 'get' and 'delete' options
        main_layout.addWidget(QLabel("Select Operation:"))
        main_layout.addWidget(self.op_combo)

        # Enter button to simulate key submission
        self.enter_button = QPushButton("Execute Operation")
        self.enter_button.clicked.connect(self.execute_operation)
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

    def execute_operation(self):
        key = self.key_input.text().strip()
        value = self.value_input.text().strip()
        operation = self.op_combo.currentText()

        if operation == "set":
            if not key or not value:
                self.status_bar.showMessage("Key and Value cannot be empty!", 3000)
                return

            try:
                response = requests.post(f"{self.server_url}/set", json={"key": key, "value": value})
                if response.status_code == 200:
                    self.status_bar.showMessage(f"SET operation successful: {key} = {value}", 3000)
                    self.key_input.clear()
                    self.value_input.clear()
                else:
                    self.status_bar.showMessage(f"Error: {response.status_code}", 3000)
            except requests.exceptions.ConnectionError:
                self.status_bar.showMessage("Error: Cannot connect to the server. Is it running?", 3000)

        elif operation == "get":
            if not key:
                self.status_bar.showMessage("Key cannot be empty for GET operation!", 3000)
                return

            try:
                response = requests.get(f"{self.server_url}/get/{key}")
                if response.status_code == 200:
                    data = response.json()
                    self.status_bar.showMessage(f"GET operation successful: {data['key']} = {data['value']}", 3000)
                elif response.status_code == 404:
                    self.status_bar.showMessage("Key not found!", 3000)
                else:
                    self.status_bar.showMessage(f"Error: {response.status_code}", 3000)
            except requests.exceptions.ConnectionError:
                self.status_bar.showMessage("Error: Cannot connect to the server. Is it running?", 3000)

        elif operation == "del":
            if not key:
                self.status_bar.showMessage("Key cannot be empty for DELETE operation!", 3000)
                return

            try:
                response = requests.delete(f"{self.server_url}/del/{key}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("deleted", False):
                        self.status_bar.showMessage(f"DELETE operation successful: {key} deleted", 3000)
                    else:
                        self.status_bar.showMessage("Key not found for deletion!", 3000)
                else:
                    self.status_bar.showMessage(f"Error: {response.status_code}", 3000)
            except requests.exceptions.ConnectionError:
                self.status_bar.showMessage("Error: Cannot connect to the server. Is it running?", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KVStoreGUI()
    window.show()
    sys.exit(app.exec_())
