import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStatusBar
from PyQt5.QtCore import Qt

class KVStoreGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False  # Initially set dark mode to False
        self.init_ui()

    def init_ui(self):
        # Set the window title and size
        self.setWindowTitle("Key-Value Store GUI - Basic Version")
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
                QStatusBar {
                    background-color: #4C566A;
                    color: #ECEFF4;
                }
            """)
            self.status_bar.showMessage("Dark mode enabled")
        else:
            self.setStyleSheet("")  # Reset to default style
            self.status_bar.showMessage("Dark mode disabled")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KVStoreGUI()
    window.show()
    sys.exit(app.exec_())
