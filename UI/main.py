import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QStatusBar, QFormLayout, 
                             QComboBox, QTableWidget, QTableWidgetItem, QSplitter)
from PyQt5.QtCore import Qt
from datetime import datetime

class KVStoreGUI(QMainWindow):
    def _init_(self):
        super()._init_()
        self.dark_mode = False
        self.server_url = "http://localhost:8080"
        self.table_data = []  # Store all operations history
        self.init_ui()

    def init_ui(self):
        # Set the window title and size
        self.setWindowTitle("Key-Value Store GUI - Enhanced")
        self.setGeometry(100, 100, 900, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Dark mode toggle button
        self.dark_mode_button = QPushButton("Toggle Dark Mode")
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        main_layout.addWidget(self.dark_mode_button)

        # Create a splitter for resizable areas
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)

        # Input section
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)

        # Operation selection
        self.op_combo = QComboBox()
        self.op_combo.addItems(["set", "get", "del"])
        input_layout.addWidget(QLabel("Select Operation:"))
        input_layout.addWidget(self.op_combo)

        # Key input
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter key here...")
        input_layout.addWidget(QLabel("Enter Key:"))
        input_layout.addWidget(self.key_input)

        # Value input (only for 'set' operation)
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Enter value here...")
        input_layout.addWidget(QLabel("Enter Value (for set operation):"))
        input_layout.addWidget(self.value_input)

        # Execute button
        self.execute_button = QPushButton("Execute Operation")
        self.execute_button.clicked.connect(self.execute_operation)
        input_layout.addWidget(self.execute_button)

        # Clear history button
        self.clear_button = QPushButton("Clear History")
        self.clear_button.clicked.connect(self.clear_table)
        input_layout.addWidget(self.clear_button)

        splitter.addWidget(input_widget)

        # Output section
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)

        # Table for operation history
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(['Timestamp', 'Operation', 'Key', 'Value'])
        output_layout.addWidget(self.result_table)

        splitter.addWidget(output_widget)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Apply initial styles
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
                QTableWidget {
                    background-color: #3B4252;
                    color: #ECEFF4;
                    gridline-color: #4C566A;
                }
                QPushButton {
                    background-color: #5E81AC;
                    color: #ECEFF4;
                }
                QLabel {
                    color: #ECEFF4;
                }
                QStatusBar {
                    background-color: #4C566A;
                    color: #ECEFF4;
                }
            """)
        else:
            self.setStyleSheet("")

    def execute_operation(self):
        operation = self.op_combo.currentText()
        key = self.key_input.text()
        if operation == "set":
            value = self.value_input.text()
            if not key or not value:
                self.status_bar.showMessage("Key and Value must be provided for SET operation!", 3000)
                return
            self.make_request("set", key, value)
        elif operation == "get":
            if not key:
                self.status_bar.showMessage("Key must be provided for GET operation!", 3000)
                return
            self.make_request("get", key)
        elif operation == "del":
            if not key:
                self.status_bar.showMessage("Key must be provided for DELETE operation!", 3000)
                return
            self.make_request("del", key)

    def make_request(self, operation, key, value=None):
        try:
            if operation == "set":
                response = requests.post(f"{self.server_url}/set", json={"key": key, "value": value})
                if response.status_code == 200:
                    self.add_to_table(operation.upper(), key, value)
                else:
                    raise Exception(f"Server error: {response.status_code}")
            elif operation == "get":
                response = requests.get(f"{self.server_url}/get/{key}")
                if response.status_code == 200:
                    data = response.json()
                    self.add_to_table(operation.upper(), key, data['value'])
                else:
                    raise Exception("Key not found")
            elif operation == "del":
                response = requests.delete(f"{self.server_url}/del/{key}")
                if response.status_code == 200:
                    self.add_to_table(operation.upper(), key, "Deleted")
                else:
                    raise Exception("Key not found")
        except requests.exceptions.ConnectionError:
            self.status_bar.showMessage("Server connection error", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}", 3000)

    def add_to_table(self, operation, key, value):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)
        self.result_table.setItem(row_position, 0, QTableWidgetItem(timestamp))
        self.result_table.setItem(row_position, 1, QTableWidgetItem(operation))
        self.result_table.setItem(row_position, 2, QTableWidgetItem(key))
        self.result_table.setItem(row_position, 3, QTableWidgetItem(str(value)))
        self.status_bar.showMessage(f"Operation {operation} executed", 3000)

    def clear_table(self):
        self.result_table.setRowCount(0)
        self.status_bar.showMessage("History cleared", 3000)


if __name__ == "_main_":
    app = QApplication(sys.argv)
    window = KVStoreGUI()
    window.show()
    sys.exit(app.exec_())