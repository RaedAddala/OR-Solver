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
        # print("Getting number of criteria")
        if self.num_criteria_edit.text().isdigit():
            num_criteria = int(self.num_criteria_edit.text())
            # print(f"Number of criteria entered: {num_criteria}")
            return num_criteria
        return 0

    def accept(self):
        # if self.name_edit.text() == '':
        #     QMessageBox.critical(
        #         self, 'Error', 'Please enter the celebrity name.')
        # elif self.salary_edit.text() == '' or not self.salary_edit.text().replace('.', '', 1).isdigit():
        #     QMessageBox.critical(
        #         self, 'Error', 'Please enter a valid salary (decimal number).')
        # elif self.mass_edit.text() == '' or not self.mass_edit.text().replace('.', '', 1).isdigit():
        #     QMessageBox.critical(
        #         self, 'Error', 'Please enter a valid mass (decimal number).')
        # elif self.value_added_edit.text() == '' or not self.value_added_edit.text().replace('.', '',
        #                                                                                     1).isdigit() or int(
        #     self.value_added_edit.text()) > 100:
        #     QMessageBox.critical(
        #         self, 'Error', 'Please enter a valid popularity index (decimal number <= 100).')
        # else:
        # print("clicked accept")
        super().accept()
