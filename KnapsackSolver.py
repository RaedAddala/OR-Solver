from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QMessageBox
from gurobipy import Model, GRB
class KnapsackSolver(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Styling
        self.setStyleSheet("font-size: 14px;")
        # Layouts
        layout = QVBoxLayout()
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.gotoHome)

        # Input
        self.capacity_input = QLineEdit("7")
        self.weights_input = QLineEdit("2,5,4,3")
        self.values_input = QLineEdit("20,30,40,50")

        layout.addWidget(QLabel("Knapsack Capacity (kg):"))
        layout.addWidget(self.capacity_input)
        layout.addWidget(QLabel("Item Values (comma-separated):"))
        layout.addWidget(self.values_input)
        layout.addWidget(QLabel("Item Weights (comma-separated):"))
        layout.addWidget(self.weights_input)

        # Solve
        solve_kp_btn = QPushButton('Solve Knapsack', self)
        solve_kp_btn.clicked.connect(self.solve_knapsack)
        layout.addWidget(solve_kp_btn)

        # Result
        self.outputArea = QTextEdit()
        self.outputArea.setReadOnly(True)
        layout.addWidget(self.outputArea)
        layout.addWidget(back_button)

        # Set Layout
        self.setLayout(layout)

    def gotoHome(self):
        self.parent.stack.setCurrentIndex(0)

    def solve_knapsack(self):
        try:
            values = list(map(int, self.values_input.text().split(',')))
            weights = list(map(int, self.weights_input.text().split(',')))
            capacity = int(self.capacity_input.text())
            n = len(values)
            n2 = len(weights)
            # Input Validation
            if not (n2 == n):
                raise InvalidInputError("Weights and Values must be of equal lengths")
            
            if not (all_positive(values)):
                raise InvalidInputError("Values must be all positive")
            
            if not (all_positive(weights)):
                raise InvalidInputError("Weights must be all positive")

            m = Model("knapsack")
            x = m.addVars(n, vtype=GRB.BINARY, name="x")
            m.setObjective(sum(values[i] * x[i] for i in range(n)), GRB.MAXIMIZE)
            m.addConstr(sum(weights[i] * x[i] for i in range(n)) <= capacity, "capacity")
            m.optimize()

            if m.status == GRB.OPTIMAL and m.objVal > 0:
                result = f"Optimal value: {m.objVal}\nSelected items:\n"
                for i in range(n):
                    if x[i].X > 0.5:  # If x[i] is 1
                        result += f"Item {i} - Value: {values[i]}, Weight: {weights[i]}\n"
                self.outputArea.setText(result)
            else:
                self.outputArea.setText("No optimal solution found.")
        except InvalidInputError as e:
            QMessageBox.critical(self, "Invalid Input Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", "Failed to solve the problem: " + str(e))

class InvalidInputError(Exception):
    pass

all_positive = lambda lst: all(value >= 0 for value in lst)
