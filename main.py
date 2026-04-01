import sys
import subprocess
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QFileDialog, QVBoxLayout,
    QMessageBox, QTextEdit
)


class OpenModelicaApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenModelica Simulation Runner")
        self.setGeometry(300, 150, 500, 400)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        # File selection
        self.label_file = QLabel("Select Simulation File (.bat)")
        self.input_file = QLineEdit()
        self.input_file.setPlaceholderText("Select .bat file")

        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.select_file)

        # Start time
        self.label_start = QLabel("Start Time")
        self.input_start = QLineEdit()
        self.input_start.setPlaceholderText("e.g. 0")

        # Stop time
        self.label_stop = QLabel("Stop Time")
        self.input_stop = QLineEdit()
        self.input_stop.setPlaceholderText("e.g. 1")

        # Run button
        self.btn_run = QPushButton("Run Simulation")
        self.btn_run.clicked.connect(self.run_model)

        # Output box (IMPORTANT)
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Simulation output will appear here...")

        # Styling
        self.btn_run.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.btn_browse.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 6px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1e88e5;
            }
        """)

        # Layout
        layout.addWidget(self.label_file)
        layout.addWidget(self.input_file)
        layout.addWidget(self.btn_browse)

        layout.addWidget(self.label_start)
        layout.addWidget(self.input_start)

        layout.addWidget(self.label_stop)
        layout.addWidget(self.input_stop)

        layout.addWidget(self.btn_run)

        layout.addWidget(QLabel("Output"))
        layout.addWidget(self.output_box)

        self.setLayout(layout)

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select BAT File",
            "",
            "Batch Files (*.bat)"
        )
        if file:
            self.input_file.setText(file)

    def run_model(self):
        file_path = self.input_file.text().strip()

        # Clear previous output
        self.output_box.clear()

        # Validation
        if not file_path:
            QMessageBox.warning(self, "Error", "Please select a .bat file")
            return

        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Error", "Selected file does not exist")
            return

        try:
            start = float(self.input_start.text())
            stop = float(self.input_stop.text())

            if not (0 <= start < stop < 5):
                raise ValueError("Ensure 0 ≤ start < stop < 5")

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
            return

        try:
            folder = os.path.dirname(file_path)

            # Run .bat
            result = subprocess.run(
                [file_path],
                cwd=folder,
                capture_output=True,
                text=True
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            # Display output in GUI
            if output:
                self.output_box.append("OUTPUT:\n" + output)

            if error:
                self.output_box.append("\nERROR:\n" + error)

            # Status popup
            if result.returncode != 0:
                QMessageBox.critical(self, "Simulation Failed", "Check output below")
            else:
                QMessageBox.information(self, "Success", "Simulation completed")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenModelicaApp()
    window.show()
    sys.exit(app.exec())