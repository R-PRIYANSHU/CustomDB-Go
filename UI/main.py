
import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QTextEdit, QLabel, QStatusBar, QComboBox, 
                            QLineEdit, QTableWidget, QTableWidgetItem, QSplitter)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os
from datetime import datetime

class KVStoreGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.server_url = "http://localhost:8080"
        self.table_data = []  # Store all operations history
        self.db_file = "kvstore_db.json"  # Assume the database is a JSON file
        self.init_ui()
        self.load_data_from_db()  # Load the data from the database when starting the app

    def init_ui(self):
        self.setWindowTitle("Key-Value Store GUI")
        self.setGeometry(100, 100, 900, 700)

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
        op_layout = QHBoxLayout()
        op_label = QLabel("Operation:")
        op_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.op_combo = QComboBox()
        self.op_combo.addItems(["set", "get", "del"])
        self.op_combo.currentTextChanged.connect(self.operation_changed)
        op_layout.addWidget(op_label)
        op_layout.addWidget(self.op_combo)
        input_layout.addLayout(op_layout)

        # Key input
        key_layout = QHBoxLayout()
        key_label = QLabel("Key:")
        self.key_input = QLineEdit()
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.key_input)
        input_layout.addLayout(key_layout)

        # Value input (only for set operation)
        value_layout = QHBoxLayout()
        value_label = QLabel("Value:")
        self.value_input = QLineEdit()
        value_layout.addWidget(value_label)
        value_layout.addWidget(self.value_input)
        input_layout.addLayout(value_layout)

        # Execute button
        button_layout = QHBoxLayout()
        self.execute_button = QPushButton("Execute")
        self.execute_button.clicked.connect(self.execute_operation)
        button_layout.addWidget(self.execute_button)

        # Clear table button
        self.clear_button = QPushButton("Clear History")
        self.clear_button.clicked.connect(self.clear_table)
        button_layout.addWidget(self.clear_button)

        # Clear database button
        self.clear_db_button = QPushButton("Clear Database")
        self.clear_db_button.clicked.connect(self.clear_db)
        button_layout.addWidget(self.clear_db_button)
        
        input_layout.addLayout(button_layout)

        splitter.addWidget(input_widget)

        # Output section
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)

        output_label = QLabel("Operation History:")
        output_label.setFont(QFont("Arial", 12, QFont.Bold))
        output_layout.addWidget(output_label)

        # Table for displaying results
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)  # Added timestamp and operation columns
        self.result_table.setHorizontalHeaderLabels(['Timestamp', 'Operation', 'Key', 'Value'])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        output_layout.addWidget(self.result_table)

        splitter.addWidget(output_widget)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        self.apply_style()
        self.operation_changed()

    def load_data_from_db(self):
        """Load the data from the database (JSON file) and populate the table."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as file:
                    db_data = json.load(file)
                    for key, value in db_data.items():
                        self.add_to_table("SET", key, value)  # Assume the operation is a "SET" for all entries
                self.status_bar.showMessage("Data loaded from the database.", 3000)
            except Exception as e:
                self.status_bar.showMessage(f"Error loading database: {str(e)}", 3000)
        else:
            self.status_bar.showMessage("No database file found. Starting fresh.", 3000)

    def execute_operation(self):
        operation = self.op_combo.currentText()
        key = self.key_input.text()
        
        if not key:
            self.status_bar.showMessage("Key cannot be empty!", 3000)
            return

        try:
            if operation == "set":
                value = self.value_input.text()
                if not value:
                    self.status_bar.showMessage("Value cannot be empty for SET operation!", 3000)
                    return
                
                response = requests.post(
                    f"{self.server_url}/set",
                    json={"key": key, "value": value}
                )
                if response.status_code == 200:
                    self.add_to_table(operation.upper(), key, value)
                    self.update_db(key, value, operation="set")  # Update the database with new key-value pair
                    self.key_input.clear()
                    self.value_input.clear()
                else:
                    raise Exception(f"Server returned status code: {response.status_code}")
                
            elif operation == "get":
                response = requests.get(f"{self.server_url}/get/{key}")
                if response.status_code == 200:
                    data = response.json()
                    self.add_to_table(operation.upper(), data["key"], data["value"])
                elif response.status_code == 404:
                    self.add_to_table(operation.upper(), key, "Not Found")
                    return
                else:
                    raise Exception(f"Server returned status code: {response.status_code}")
                
            elif operation == "del":
                response = requests.delete(f"{self.server_url}/del/{key}")
                if response.status_code == 200:
                    data = response.json()
                    if data["deleted"]:
                        self.add_to_table(operation.upper(), key, "Deleted")
                        self.update_db(key, None, operation="del")  # Remove the key from the local database
                        self.key_input.clear()
                    else:
                        self.add_to_table(operation.upper(), key, "Not Found")
                        return
                else:
                    raise Exception(f"Server returned status code: {response.status_code}")

            self.status_bar.showMessage(f"Operation {operation} executed successfully", 3000)
            
        except requests.exceptions.ConnectionError:
            self.status_bar.showMessage("Error: Cannot connect to the server. Is it running?", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}", 3000)

    def update_db(self, key, value, operation):
        """Update the database file with a new key-value pair, or delete the key if operation is 'del'."""
        db_data = {}
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as file:
                db_data = json.load(file)

        if operation == "set":
            db_data[key] = value  # Add or update the key-value pair
        elif operation == "del":
            if key in db_data:
                del db_data[key]  # Remove the key from the database

        with open(self.db_file, "w") as file:
            json.dump(db_data, file)


    def add_to_table(self, operation, key, value):
        """Add new entry to the result table with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.table_data.append((timestamp, operation, key, value))
        self.update_table_display()

    def update_table_display(self):
        """Refresh the table display with current data."""
        self.result_table.setRowCount(len(self.table_data))
        for row, (timestamp, operation, key, value) in enumerate(self.table_data):
            self.result_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.result_table.setItem(row, 1, QTableWidgetItem(operation))
            self.result_table.setItem(row, 2, QTableWidgetItem(key))
            self.result_table.setItem(row, 3, QTableWidgetItem(value))

    def clear_table(self):
        """Clear the operation history table."""
        self.table_data = []
        self.result_table.setRowCount(0)
        self.status_bar.showMessage("Table cleared", 3000)

    def clear_db(self):
        """Clear all the data stored in the database file."""
        with open(self.db_file, "w") as file:
            json.dump({}, file)
        self.table_data = []  # Clear the table data as well
        self.update_table_display()  # Refresh the table
        self.status_bar.showMessage("Database cleared", 3000)

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
                QTableWidget QHeaderView::section {
                    background-color: #4C566A;
                    color: #ECEFF4;
                    border: 1px solid #2E3440;
                }
                QLineEdit, QComboBox {
                    background-color: #3B4252;
                    color: #ECEFF4;
                    border: 1px solid #4C566A;
                    border-radius: 4px;
                    padding: 5px;
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
                QLabel {
                    color: #ECEFF4;
                }
                QStatusBar {
                    background-color: #4C566A;
                    color: #ECEFF4;
                }
                QSplitter::handle {
                    background-color: #4C566A;
                }
            """)
        else:
            self.setStyleSheet("""
                QSplitter::handle {
                    background-color: #CCCCCC;
                }
            """)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_style()


    def operation_changed(self):
        """Adjust the UI based on the selected operation."""
        operation = self.op_combo.currentText()
        if operation == "set":
            self.value_input.setEnabled(True)
        else:
            self.value_input.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KVStoreGUI()
    window.show()
    sys.exit(app.exec_())