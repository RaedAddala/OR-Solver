from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout


class CriteriaInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ok_button = None
        self.num_criteria_edit = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Criteria Input')
        layout = QVBoxLayout()

        self.num_criteria_edit = QLineEdit()
        self.num_criteria_edit.setPlaceholderText('Enter number of criteria')

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(QLabel('Enter the number of criteria:'))
        layout.addWidget(self.num_criteria_edit)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def getNumCriteria(self):
        if self.num_criteria_edit.text().isdigit():
            num_criteria = int(self.num_criteria_edit.text())
            return num_criteria
        return 0
