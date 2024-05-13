from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QLineEdit, QInputDialog
from PyQt5.QtCore import Qt

from CriteriaInputDialog import CriteriaInputDialog
from VariableInputDialog import VariableInputDialog


class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        title_layout = QVBoxLayout()
        description_layout = QVBoxLayout()
        problems_layout = QHBoxLayout()
        title_label = QLabel("HOME PAGE")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight:light; font-size: 15px;  color: #555555;  ")  # Added margin-bottom

        welcome_label = QLabel("- Welcome to our Operational Research project -")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet(" font-size: 28px; font-weight:bold;color:#2980b9 ")

        description_label = QLabel(
            "where we tackle optimization challenges in both Selection and Transportation problems to enhance \n decision-making and resource allocation efficiency.")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("font-weight:semi-weight; font-size: 24px;  ")

        # //////////////////////////////////////////////////////////
        btn_selection = QPushButton('Selection Problem')
        btn_selection.setFixedSize(300, 70)
        btn_selection.setCursor(Qt.PointingHandCursor)
        btn_selection.setStyleSheet(
            "QPushButton {"
            "   font-size: 19px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size:21px;"
            "}"
        )
        btn_selection.clicked.connect(self.showSelectionPopup)

        # //////////////////////////////////////////////////////////
        btn_transportation = QPushButton('Transportation Problem')
        btn_transportation.setFixedSize(300, 70)
        btn_transportation.setCursor(Qt.PointingHandCursor)
        btn_transportation.setStyleSheet(
            "QPushButton {"
            "   font-size: 19px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size: 21px;"
            "}"
        )
        btn_transportation.clicked.connect(lambda: self.parent.show_page("Transportation"))

        title_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignTop)  # Align the title_label to the top
        description_layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignTop)
        description_layout.addWidget(description_label, alignment=Qt.AlignmentFlag.AlignTop)
        problems_layout.addWidget(btn_selection)
        problems_layout.addWidget(btn_transportation)
        problems_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(description_layout)
        main_layout.addLayout(problems_layout)
        description_layout.setContentsMargins(50, 0, 50, 50)  # Adjust the top and bottom margins of main_layout

        main_layout.setContentsMargins(50, 0, 50, 50)  # Adjust the top and bottom margins of main_layout

        self.setLayout(main_layout)

    # ////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////// Selection problem methods 🔽🔽
    # opens dialog before Selection Problem Page
    def showSelectionPopup(self):
        # fetch the name of the gain coefficient
        self.parent.selectionProblem.gain_name = self.getGainName()
        # fetch the number and names of constraints
        dialog = CriteriaInputDialog(self)
        criteria_names = []
        if dialog.exec_():
            num_criteria = int(dialog.getNumCriteria())
            if num_criteria > 0:
                criteria_names = self.getConstraintNames(num_criteria)
                if criteria_names:
                    self.parent.selectionProblem.setupCriteriaFields(criteria_names)
        # fetch the number and names of variables
        dialog = VariableInputDialog(self)
        if dialog.exec_():
            num_vars = int(dialog.getNumCriteria())
            if num_vars > 0:
                var_names = self.getVariableNames(num_vars)
                if var_names:
                    for vname in var_names:
                        self.parent.selectionProblem.setupVariableFields(criteria_names, vname)
                    self.parent.show_page("Selection")

    # methods to fetch the names of constraints, variables
    # and the gain coefficient
    def getConstraintNames(self, num_criteria):
        names = []
        for i in range(num_criteria):
            name, ok = QInputDialog.getText(self, f'Enter name for Criterion {i + 1}', 'Criterion Name:')
            if ok:
                names.append(name)
        return names

    def getVariableNames(self, num_vars):
        names = []
        for i in range(num_vars):
            name, ok = QInputDialog.getText(self, f'Enter name for variable {i + 1}', 'Variable Name:')
            if ok:
                names.append(name)
        return names

    def getGainName(self):
        name, ok = QInputDialog.getText(self, f'Enter name for gain', 'Gain Name:')
        return name if ok else "Gain"
    # //////////////////////////////////// Selection problem methods 🔼🔼
