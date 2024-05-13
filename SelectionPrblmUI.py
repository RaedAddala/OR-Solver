import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QListWidget, QListWidgetItem, QCheckBox, QMessageBox, QDialog, QDialogButtonBox

from GurobiSolver import GurobiSolverBuilder
from gurobipy import GRB
import gurobipy as gp

# GUI styles
style_sheet = """
    QWidget {
        background-color: white;
    }
    QLineEdit {
        background-color: #f0f0f0; /* Light gray */
        border: 1px solid #ccc; /* Light gray border */
        border-radius: 3px;
        padding: 5px;
    }
    QLineEdit:focus {
        border-color: #33a6cc; /* Focus color */
    }
    QPushButton {
        background-color: #BED7DC; /* Light purple */
        color: white;
        font-size: 16px;
        padding: 5px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #B3C8CF; /* Dark purple */
    }
    QPushButton:pressed {
        background-color: #496989; /* Even darker purple */
    }
    QPushButton.remove_btn {
        background-color: #FF4D4D; /* Red */
        color: white;
    }

    SolveButton:pressed {
        background-color: #C6EBC5; /* Green */
        color: white;
    }
    DeleteButton{
        background-color:#DD5746
    }
    DeleteButton:hover{
    background-color:rgb(190,39,39)
    }
    DeleteButton:pressed{
        background-color:black
    }"""


class SelectionPrblmUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = None
        self.min_vip_edit = None
        self.min_vip_label = None
        self.criteria_edits = []
        self.criteria_labels = []
        self.parent = parent
        self.initUI()
        self.problem_relationships = {}  # Dictionary to store problem relationships

    def initUI(self):
        self.setWindowTitle('Who will be your celebrity guests?')
        self.resize(800, 500)

        self.min_vip_label = QLabel('Minimum VIP Celebrities:')
        self.min_vip_edit = QLineEdit()
        self.min_vip_edit.setPlaceholderText('Enter minimum number...')
        # Layout for minimum VIP input
        vip_layout = QHBoxLayout()
        vip_layout.addWidget(self.min_vip_label)
        vip_layout.addWidget(self.min_vip_edit)

        button1 = QPushButton(
            'Go back to Home Page')
        button1.setStyleSheet(
            "font-size: 16px; font-family: 'Arial'; color: #233154 ; padding: 10px;font-weight: bold;")
        button1.clicked.connect(self.open_homepage)

        # Widgets for ship weight and budget input
        # self.weight_label = QLabel('Total ship weight (Kg):')
        # self.weight_edit = QLineEdit()
        #
        # self.budget_label = QLabel('Maximum budget ($):')
        # self.budget_edit = QLineEdit()

        self.add_celebrity_button = QPushButton('Add Celebrity')
        self.add_celebrity_button.clicked.connect(self.addCelebrity)

        self.find_celebrity_list_button = QPushButton(
            'Find the optimal guest list')
        self.find_celebrity_list_button.clicked.connect(self.findCelebrityList)

        # Summary label widgets
        self.summary_label = QLabel('Optimal guest list and statistics:')
        self.summary_text = QListWidget()
        self.summary_label.setVisible(False)
        self.summary_text.setVisible(False)

        # Celebrity list widget
        self.celebrity_list_label = QLabel('List of all celebrities')
        self.celebrity_list = QListWidget()
        self.celebrity_list.setSelectionMode(
            QListWidget.MultiSelection)  # Enable multiple selection

        # Button to open criteria input dialog
        # self.criteria_button = QPushButton('Input Criteria')
        # self.criteria_button.clicked.connect(self.openCriteriaInputDialog)

        # # Layout for ship weight input
        # input_layout = QHBoxLayout()
        # input_layout.addWidget(self.weight_label)
        # input_layout.addWidget(self.weight_edit)
        #
        # # Layout for budget input
        # input_layout.addWidget(self.budget_label)
        # input_layout.addWidget(self.budget_edit)

        # Layout for adding celebrities and finding the optimal list
        button_layout = QHBoxLayout()
        # Add the button to the layout
        # button_layout.addWidget(self.criteria_button)
        button_layout.addWidget(self.add_celebrity_button)
        button_layout.addWidget(self.find_celebrity_list_button)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(button1)
        # main_layout.addLayout(input_layout)
        self.main_layout.addLayout(vip_layout)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.summary_label)
        self.main_layout.addWidget(self.summary_text)
        self.main_layout.addWidget(self.celebrity_list_label)
        self.main_layout.addWidget(self.celebrity_list)

        self.setLayout(self.main_layout)

    def setupCriteriaFields(self, criteria_names):
        for name in criteria_names:
            label = QLabel(f'Upper limit for {name}:')
            edit = QLineEdit()
            criteria_layout = QHBoxLayout()
            criteria_layout.addWidget(label)
            criteria_layout.addWidget(edit)
            self.criteria_labels.append(label)
            self.criteria_edits.append(edit)
            # self.main_layout.addWidget(label)
            # self.main_layout.addWidget(edit)
            self.main_layout.addLayout(criteria_layout)

    def setupVariableFields(self, criteria_names, variable_name="placeholder",gain_name="win"):
        vlabel = QLabel(variable_name)
        self.main_layout.addWidget(vlabel)
        vedit_layout = QHBoxLayout()
        for name in criteria_names:
            clabel = QLabel(f'{name}:')
            cedit = QLineEdit()
            criteria_layout = QVBoxLayout()
            criteria_layout.addWidget(clabel)
            criteria_layout.addWidget(cedit)
            vedit_layout.addLayout(criteria_layout)
        vgain_layout = QVBoxLayout()
        vgain_layout.addWidget(QLabel(gain_name))
        vgain_layout.addWidget(QLineEdit())
        vedit_layout.addLayout(vgain_layout)
        self.main_layout.addLayout(vedit_layout)

    def addCelebrity(self):
        celebrity_dialog = CelebrityDialog(self)
        existing_celebrities = [self.celebrity_list.item(i).text().split(
            ' - ')[0] for i in range(self.celebrity_list.count())]
        celebrity_dialog.updateProblemsWithList(existing_celebrities)

        if celebrity_dialog.exec_() == QDialog.Accepted:
            name = celebrity_dialog.name_edit.text()
            salary = float(celebrity_dialog.salary_edit.text())
            mass = float(celebrity_dialog.mass_edit.text())
            popularity = float(celebrity_dialog.value_added_edit.text())
            is_vip = celebrity_dialog.vip_checkbox.isChecked()
            problems_with_items = celebrity_dialog.problems_with_list.selectedItems()
            problems_with = [
                item.text() for item in problems_with_items] if problems_with_items else None
            self.addCelebrityToList(
                name, salary, mass, popularity, is_vip, problems_with)

    def addCelebrityToList(self, name, salary, mass, popularity, is_vip, problems_with):
        item_text = f'{name} - Salary: {salary} - Mass: {mass} - Popularity Index: {popularity} - VIP: {is_vip}'
        if problems_with:
            problems_with_str = ' - Problems with: ' + ', '.join(problems_with)
            item_text += problems_with_str
            # Update problem relationships dictionary
            self.problem_relationships[name] = problems_with
        item = QListWidgetItem(item_text)
        item.setData(1000, (name, salary, mass,
                            popularity, is_vip, problems_with))
        self.celebrity_list.addItem(item)

    def findCelebrityList(self):
        total_celebrities = self.celebrity_list.count()

        if total_celebrities == 0:
            QMessageBox.warning(self, 'Warning', 'Please add at least one celebrity.')
            return

        # Validate ship weight
        ship_weight_text = self.weight_edit.text()
        if not ship_weight_text or not ship_weight_text.replace('.', '', 1).isdigit() or float(ship_weight_text) <= 0:
            QMessageBox.warning(self, 'Invalid Value', 'Ship weight must be a positive value.')
            return
        ship_weight = float(ship_weight_text)

        # Validate budget
        budget_text = self.budget_edit.text()
        if not budget_text or not budget_text.replace('.', '', 1).isdigit() or float(budget_text) <= 0:
            QMessageBox.warning(self, 'Invalid Value', 'Maximum budget must be a positive value.')
            return
        budget = float(budget_text)

        # Retrieve minimum number of VIP celebrities from the input field
        try:
            min_vip_count = int(self.min_vip_edit.text())
            if min_vip_count < 0:
                QMessageBox.warning(self, 'Invalid Value', 'Minimum VIP count must be a non-negative integer.')
                return
        except ValueError:
            QMessageBox.warning(self, 'Invalid Value', 'Please enter a valid integer for minimum VIP count.')
            return

        # Build Gurobi model
        builder = GurobiSolverBuilder()
        solver_builder = builder.add_variables(total_celebrities, names=[f'x_{i}' for i in range(total_celebrities)],
                                               vtypes=[GRB.BINARY] * total_celebrities)

        constraints_LHS = []
        constraints_RHS = [ship_weight, budget, -1]
        popularities = []
        negative_salaries = []
        exists_in_boat = []

        for i in range(total_celebrities):
            item_text = self.celebrity_list.item(i).text()
            salary = float(item_text.split(' - ')[1].split(': ')[1])
            mass = float(item_text.split(' - ')[2].split(': ')[1])
            popularity = float(item_text.split(' - ')[3].split(': ')[1])
            vip_status = item_text.split(' - ')[4].split(': ')[1] == 'True'

            constraints_LHS.append([mass, salary, -int(vip_status)])
            negative_salaries.append(-salary)
            popularities.append(popularity)
            exists_in_boat.append(1)

        objectives = [
            (popularities, GRB.MAXIMIZE),
            (negative_salaries, GRB.MAXIMIZE),
            (exists_in_boat, GRB.MAXIMIZE)
        ]

        # Build the solver instance
        solver = solver_builder.set_objectives(objectives).set_constraints_LHS(constraints_LHS).set_constraints_RHS(
            constraints_RHS).build()

        # Add constraint to ensure at least min_vip_count VIP celebrities are selected
        vip_indices = [i for i in range(total_celebrities) if self.celebrity_list.item(i).text().endswith('VIP: True')]
        if solver:
            vip_count_expr = gp.quicksum(solver.decision_variables[idx] for idx in vip_indices)
            solver.add_constraint(vip_count_expr, GRB.GREATER_EQUAL, min_vip_count)

            # Mutual exclusion constraint based on problem relationships
            for celeb, problems in self.problem_relationships.items():
                celeb_index = next(
                    (i for i in range(total_celebrities) if self.celebrity_list.item(i).text().startswith(celeb)), None)
                if celeb_index is not None:
                    related_indices = [i for i in range(total_celebrities) if
                                       any(self.celebrity_list.item(i).text().startswith(p) for p in problems)]
                    if related_indices:
                        # If celeb is selected, none of the related_indices should be selected
                        expr = gp.LinExpr()

                        # Add the celebrity variable (xi) with its coefficient as the number of related problems
                        expr.add(solver.decision_variables[celeb_index], len(related_indices))

                        # Add related variables (xj) with a coefficient of 1 each
                        for idx in related_indices:
                            expr.add(solver.decision_variables[idx], 1)

                        # Add the constraint that ensures the total count is less than or equal to the number of related problems
                        solver.add_constraint(expr, GRB.LESS_EQUAL, len(related_indices))

            # Solve the optimization problem
            solver.solve()
            solution_status = solver.get_solution_status()

            # Process the solution if optimal
            if solution_status == GRB.OPTIMAL:
                solution_values = solver.get_variables()
                self.displayOptimalGuestList(solution_values)
            else:
                QMessageBox.warning(self, 'Warning', 'No optimal solution found.')
        else:
            QMessageBox.warning(self, 'Error', 'Failed to build Gurobi solver instance.')

    def displayOptimalGuestList(self, solution_values):
        self.summary_text.clear()
        self.summary_label.setVisible(True)
        self.summary_text.setVisible(True)

        selected_celebrities = []
        total_people = 0
        total_popularity = 0.0
        total_mass = 0.0
        total_salary = 0.0
        vip_celebrities = []
        non_vip_celebrities = []

        # Iterate over the decision variables and gather statistics for selected celebrities
        for i in range(self.celebrity_list.count()):
            item = self.celebrity_list.item(i)
            if not item:
                continue

            celebrity_name = item.text().split(' - ')[0]
            if f'x_{i}' in solution_values and solution_values[f'x_{i}'] > 0.5:
                selected_celebrities.append(celebrity_name)

                # Retrieve celebrity attributes
                salary_str = item.text().split(' - ')[1].split(': ')[1]
                mass_str = item.text().split(' - ')[2].split(': ')[1]
                popularity_str = item.text().split(' - ')[3].split(': ')[1]
                vip_status = item.text().split(' - ')[4].split(': ')[1]

                try:
                    salary_value = float(salary_str)
                    mass_value = float(mass_str)
                    popularity_value = float(popularity_str)
                    is_vip = vip_status == 'True'

                    # Calculate totals
                    total_people += 1
                    total_salary += salary_value
                    total_mass += mass_value
                    total_popularity += popularity_value

                    # Categorize celebrities
                    if is_vip:
                        vip_celebrities.append(celebrity_name)
                    else:
                        non_vip_celebrities.append(celebrity_name)

                except ValueError as e:
                    print(f"Error processing celebrity item: {item.text()}. Error: {e}")

        if selected_celebrities:
            # Display total statistics based on selected celebrities
            self.summary_text.addItem(f"Total Number of People: {total_people}")
            self.summary_text.addItem(
                f"Average Popularity Index: {total_popularity / total_people if total_people > 0 else 0.0}%")
            self.summary_text.addItem(f"Total Mass: {total_mass} Kg")
            self.summary_text.addItem(f"Total Salary: ${total_salary}")
            self.summary_text.addItem(
                f"-------------------------------------------------------------------------------")
            if vip_celebrities:
                self.summary_text.addItem("VIP Celebrities:")
                for vip in vip_celebrities:
                    self.summary_text.addItem(vip)
                self.summary_text.addItem(
                    f"-------------------------------------------------------------------------------")
            if non_vip_celebrities:
                self.summary_text.addItem("Non-VIP Celebrities:")
                for non_vip in non_vip_celebrities:
                    self.summary_text.addItem(non_vip)
                self.summary_text.addItem(
                    f"-------------------------------------------------------------------------------")
            self.summary_text.addItem("Selected Celebrities:")
            for celebrity in selected_celebrities:
                self.summary_text.addItem(celebrity)
        else:
            self.summary_text.addItem("No celebrities selected.")

    def open_homepage(self):
        self.parent.stack.setCurrentIndex(0)


class CelebrityDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add a Celebrity')
        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.salary_edit = QLineEdit()
        self.mass_edit = QLineEdit()
        self.value_added_edit = QLineEdit()
        self.vip_checkbox = QCheckBox('VIP')
        self.problems_with_label = QLabel('Problems with:')
        self.problems_with_list = QListWidget()
        self.problems_with_list.setSelectionMode(
            QListWidget.MultiSelection)  # Enable multiple selection

        layout.addWidget(QLabel('Celebrity Name:'))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel('Requested Salary ($):'))
        layout.addWidget(self.salary_edit)
        layout.addWidget(QLabel('Celebrity Mass (Kg):'))
        layout.addWidget(self.mass_edit)
        layout.addWidget(QLabel('Popularity Index (/100):'))
        layout.addWidget(self.value_added_edit)
        layout.addWidget(self.vip_checkbox)
        layout.addWidget(self.problems_with_label)
        layout.addWidget(self.problems_with_list)

        # Create button box with OK and Cancel buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def updateProblemsWithList(self, existing_celebrities):
        self.problems_with_list.clear()
        self.problems_with_list.addItems(existing_celebrities)

    def accept(self):
        if self.name_edit.text() == '':
            QMessageBox.critical(
                self, 'Error', 'Please enter the celebrity name.')
        elif self.salary_edit.text() == '' or not self.salary_edit.text().replace('.', '', 1).isdigit():
            QMessageBox.critical(
                self, 'Error', 'Please enter a valid salary (decimal number).')
        elif self.mass_edit.text() == '' or not self.mass_edit.text().replace('.', '', 1).isdigit():
            QMessageBox.critical(
                self, 'Error', 'Please enter a valid mass (decimal number).')
        elif self.value_added_edit.text() == '' or not self.value_added_edit.text().replace('.', '',
                                                                                            1).isdigit() or int(
            self.value_added_edit.text()) > 100:
            QMessageBox.critical(
                self, 'Error', 'Please enter a valid popularity index (decimal number <= 100).')
        else:
            super().accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # apply styles
    app.setStyleSheet(style_sheet)
    window = SelectionPrblmUI()
    window.show()
    sys.exit(app.exec_())
