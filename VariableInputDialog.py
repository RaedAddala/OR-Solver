from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout


class VariableInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ok_button = None
        self.num_criteria_edit = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Variables')
        self.setMinimumWidth(250)

        layout = QVBoxLayout()

        self.num_criteria_edit = QLineEdit()
        self.num_criteria_edit.setPlaceholderText('3')

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(QLabel('Enter the number of variables:'))
        layout.addWidget(self.num_criteria_edit)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)
        # Apply styles
        self.setStyleSheet("""
                    CriteriaInput {
                        background-color: #f0f0f0;
                        padding: 10px;
                        width:500px;
                    }
                    QLineEdit {
                        background-color: white;
                        border: 1px solid #ccc;
                        border-radius: 3px;
                        padding: 5px;
                    }
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)

    def getNumCriteria(self):
        # print("Getting number of criteria")
        if self.num_criteria_edit.text().isdigit():
            num_criteria = int(self.num_criteria_edit.text())
            # print(f"Number of criteria entered: {num_criteria}")
            return num_criteria
        return 0
