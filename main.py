from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea
from db import DatabaseManager
from test import MainWindow1
import json
import sys
import os

class Secure_word:
    db = DatabaseManager()
    __word = db.fetch_data_kenflix()
    def secure_word(self):
        if self.__word == ["2"]:
            app = QApplication(sys.argv)
            window = MainWindow()
            window.setGeometry(100, 100, 800, 600)
            window.setWindowTitle("Crypto Trading Inputs")
            window.show()
            sys.exit(app.exec_())
            
        else:
            data = self.db.fetch_data_message()
            
            for word in data:
                
                app = QApplication(sys.argv)
                widget = QWidget()
                QMessageBox.warning(widget, "Security Alert", word)
                sys.exit(app.exec_())

class InputGroup(QWidget):
    def __init__(self, label, fields, parent=None):
        super().__init__(parent)
        self.label = label
        self.fields = fields
        self.setup_ui()
        

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QLabel {
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #aaa;
                border-radius: 3px;
            }
            QPushButton {
                padding: 5px 10px;
                border: 1px solid #007bff;
                border-radius: 3px;
                background-color: #007bff;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
                border-color: #0056b3;
            }
        """)

        self.layout = QVBoxLayout()
        group_box = QGroupBox(self.label)

        self.field_layout = QVBoxLayout()
        self.input_widgets = {}

        for field_label in self.fields:
            input_label = QLabel(field_label)
            input_field = QLineEdit()
            self.field_layout.addWidget(input_label)
            self.field_layout.addWidget(input_field)
            self.input_widgets[field_label] = input_field

        group_box.setLayout(self.field_layout)
        self.layout.addWidget(group_box)

        self.edit_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.toggle_edit_submit)
        self.edit_layout.addWidget(self.edit_button)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_inputs)
        self.edit_layout.addWidget(self.submit_button)
        self.layout.addLayout(self.edit_layout)

        self.setLayout(self.layout)

    def toggle_edit_submit(self):
        self.edit_button.setVisible(False)
        self.submit_button.setVisible(True)
        for input_widget in self.input_widgets.values():
            input_widget.setVisible(True)

    def submit_inputs(self):
        inputs = {}
        for field_label, input_widget in self.input_widgets.items():
            inputs[field_label] = input_widget.text()
            input_widget.setVisible(False)
        self.edit_button.setVisible(True)
        self.submit_button.setVisible(False)
        print(f"Submit {self.label}: {inputs}")
        save_to_json(inputs, self.label)


def save_to_json(data, label):
    filename = f"my_db/{label.lower().replace(' ', '_')}.json"
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        app = QApplication.instance()
        app.aboutToQuit.connect(self.cleanup_on_exit)

    def setup_ui(self):
        layout = QVBoxLayout()

        input_groups = [
            ("Time for Purchase", ["Year", "Month", "Day", "Hour", "Minute", "Second"]),
            ("Buy Amount", ["Amount1", "Amount2", "Amount3", "Amount4"]),
            ("Sell When Price % Reach", ["Coin1", "Coin2", "Coin3", "Coin4"])
        ]

        for label, fields in input_groups:
            input_group = InputGroup(label, fields)
            layout.addWidget(input_group)

        continue_button = QPushButton("Continue")
        continue_button.clicked.connect(self.open_main_window_1)  

        layout.addWidget(continue_button)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)

        scroll_area.setWidget(scroll_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
    def open_main_window_1(self):
        try:
            # Create a dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("MainWindow1")

            # Set MainWindow1 as the central widget of the dialog
            window1 = MainWindow1()
            dialog_layout = QVBoxLayout()
            dialog_layout.addWidget(window1)
            dialog.setLayout(dialog_layout)
            dialog.resize(500, 400)

            # Show the dialog
            dialog.exec_()

        except Exception as e:
            print("An error occurred:", e)

        finally:
            # Ensure the dialog is properly closed
            dialog.deleteLater()
    def cleanup_on_exit(self):
        # Delete JSON files
        for filename in os.listdir():
            if filename.endswith(".json"):
                os.remove(filename)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    word = Secure_word()
    word.secure_word()
    sys.exit(app.exec_())
