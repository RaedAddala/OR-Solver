import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QListWidget, QMessageBox, QFrame

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
    QLabel {
        background-color:none;
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
    """


class SelectionPrblmUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.constraints_layout = QHBoxLayout()
        self.variables_layout = QVBoxLayout()
        self.criteria_labels = []
        self.summary_label = None
        self.summary_text = None
        self.solve_button = None
        self.criteria_edits = []
        self.variable_edits = {}
        self.main_layout = None
        self.gain_name = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Selection Problem')
        self.resize(800, 500)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color:none;")

        home_button = QPushButton(
            'Go back to Home Page')
        home_button.setStyleSheet(
            "font-size: 16px; font-family: 'Arial'; color: #233154 ; padding: 10px;font-weight: bold;")
        home_button.clicked.connect(self.open_homepage)

        # solve button widget
        self.solve_button = QPushButton('Solve')
        self.solve_button.clicked.connect(self.solve_selection)
        self.solve_button.setStyleSheet("""
            background-color: #C6EBC5; /* Green */
            color: black;
            padding:16px;
        """)

        # Summary widgets
        self.summary_label = QLabel('Selection Result :')
        self.summary_text = QListWidget()
        self.summary_label.setStyleSheet("font-size:22px;")

        # Main layout
        self.main_layout = QVBoxLayout()
        c_title = QLabel("Constraints")
        c_title.setStyleSheet("font-size:22px;")
        self.main_layout.addWidget(c_title)
        self.main_layout.addLayout(self.constraints_layout)
        self.main_layout.addWidget(line)
        v_title = QLabel("Variables")
        v_title.setStyleSheet("font-size:22px;")
        self.main_layout.addWidget(v_title)
        self.main_layout.addLayout(self.variables_layout)
        self.main_layout.addWidget(self.solve_button)
        self.main_layout.addWidget(self.summary_label)
        self.main_layout.addWidget(self.summary_text)
        self.main_layout.addWidget(home_button)

        self.setLayout(self.main_layout)
        self.setStyleSheet(style_sheet)

    # returns to home
    def open_homepage(self):
        self.criteria_labels = []
        self.summary_label = None
        self.summary_text = None
        self.solve_button = None
        self.criteria_edits = []
        self.variable_edits = {}
        self.main_layout = None
        self.gain_name = ""
        self.parent.stack.setCurrentIndex(0)

    # creates fields to input the max of each constraint
    def setupCriteriaFields(self, criteria_names):
        for name in criteria_names:
            label = QLabel(f'Upper limit for {name}:')
            label.setStyleSheet("font-size:18px;")
            edit = QLineEdit()
            criteria_layout = QHBoxLayout()
            criteria_layout.addWidget(label)
            criteria_layout.addWidget(edit)
            self.criteria_labels.append(name)
            self.criteria_edits.append(edit)
            self.constraints_layout.addLayout(criteria_layout)

    # creates fields for each variable's coefficients
    def setupVariableFields(self, criteria_names, variable_name="placeholder"):
        self.variable_edits[str(variable_name)] = {}
        vlabel = QLabel(variable_name)
        vlabel.setStyleSheet("font-style:bolder;font-size:18px;")
        self.variables_layout.addWidget(vlabel)
        vedit_layout = QHBoxLayout()
        constraint_edits = []
        for name in criteria_names:
            clabel = QLabel(name)
            cedit = QLineEdit()
            constraint_edits.append(cedit)
            criteria_layout = QVBoxLayout()
            criteria_layout.addWidget(clabel)
            criteria_layout.addWidget(cedit)
            vedit_layout.addLayout(criteria_layout)

        vgain_layout = QVBoxLayout()
        gain_edit = QLineEdit()
        gain_label = QLabel(self.gain_name)
        gain_label.setStyleSheet("font-style:italic;")
        vgain_layout.addWidget(gain_label)
        vgain_layout.addWidget(gain_edit)
        vedit_layout.addLayout(vgain_layout)
        self.variable_edits[str(variable_name)]["constraints"] = constraint_edits
        self.variable_edits[str(variable_name)]["gain"] = gain_edit
        self.variables_layout.addLayout(vedit_layout)
        self.setLayout(self.main_layout)

    # returns dict of constraint_name:max_value
    def getConstraintValues(self):
        constraint_values = {}
        for label, constraint in zip(self.criteria_labels, self.criteria_edits):
            constraint_values[label] = int(constraint.text())
        print(constraint_values)
        return constraint_values

    # returns a dict of <var_name>:{
    #   'ccoef':{
    #       <constraint_name>:<coef>
    #       },
    #   'gcoef':<gain_value>
    # }
    def getVariableValues(self):
        res = {}
        for name, var_dict in self.variable_edits.items():
            constraint_vals = {}
            for cname, c in zip(self.criteria_labels, var_dict["constraints"]):
                constraint_vals[cname] = int(c.text())
            gain_val = int(var_dict["gain"].text())
            res[name] = {"ccoef": constraint_vals, "gcoef": gain_val}
        print(res)
        return res

    # creates & solves model
    def solve_selection(self):
        try:
            data = self.getVariableValues()
            # Create a new model
            model = gp.Model()
            # Create decision variables for each variable
            variables = {}
            for var_name, var_data in data.items():
                variables[var_name] = model.addVar(vtype=GRB.BINARY, name=var_name)
            # Set objective function
            model.setObjective(sum(var_data['gcoef'] * variables[var_name] for var_name, var_data in data.items()),
                               GRB.MAXIMIZE)
            # Add constraints
            for constraint_name in self.criteria_labels:
                constraint_limit = self.getConstraintValues()[constraint_name]
                constraint_expr = sum(
                    var_data['ccoef'][constraint_name] * variables[var_name] for var_name, var_data in data.items())
                model.addConstr(constraint_expr <= constraint_limit)
            # Optimize the model
            model.optimize()
            # Print results
            if model.status == GRB.OPTIMAL:
                print('Optimal solution found:')
                for var_name, var in variables.items():
                    print(f'{var_name}: {var.X}')
                self.displaySelection(variables)
            else:
                print('No solution found')
        except InvalidInputError as e:
            QMessageBox.critical(self, "Invalid Input Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", "Failed to solve the problem: " + str(e))

    # displays solved result
    def displaySelection(self, solution_values):
        self.summary_text.clear()
        selected_vars = []
        for var_name, var in solution_values.items():
            if var.X > 0.5:
                selected_vars.append(var_name)
        if selected_vars:
            for s in selected_vars:
                self.summary_text.addItem(s)
        else:
            self.summary_text.addItem("None selected.")


class InvalidInputError(Exception):
    pass


all_positive = lambda lst: all(value >= 0 for value in lst)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # apply styles
    # app.setStyleSheet(style_sheet)
    window = SelectionPrblmUI()
    window.show()
    sys.exit(app.exec_())
