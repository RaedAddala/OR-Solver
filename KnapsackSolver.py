from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QMessageBox
from gurobipy import Model, GRB
from PyQt5.QtCore import Qt

class KnapsackSolver(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Styling
        self.setStyleSheet("font-size: 16px;")
        # Layouts
        back_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        main_layout = QVBoxLayout()
        result_layout = QVBoxLayout()



        # Back Button
        back_button = QPushButton("Back")
        back_button.setFixedSize(330, 30)
        back_button.setCursor(Qt.PointingHandCursor)  
        back_button.setStyleSheet(
             "QPushButton {"
            "   font-size: 14px;"
            "   border-radius: 10px;"
            "   background-color: #C8CECF;"
            "   color: #ffffff;"
            "   font-style: italic;"
            "}"
            "QPushButton:hover {"
            "   background-color: #BABFC0;"
            "   font-size:15px;"
            "}"
        )
        back_button.clicked.connect(self.gotoHome)
        back_layout.addWidget(back_button)
        back_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input
        self.capacity_input = QLineEdit("7")
        self.weights_input = QLineEdit("2,5,4,3")
        self.values_input = QLineEdit("20,30,40,50")

        input_layout.addWidget(QLabel("Knapsack Capacity (kg):"))
        input_layout.addWidget(self.capacity_input)
        input_layout.addWidget(QLabel("Item Values (comma-separated):"))
        input_layout.addWidget(self.values_input)
        input_layout.addWidget(QLabel("Item Weights (comma-separated):"))
        input_layout.addWidget(self.weights_input)

        # Solve

        solve_kp_btn = QPushButton('Solve Knapsack', self)
        solve_kp_btn.setFixedSize(250, 50)
        solve_kp_btn.setCursor(Qt.PointingHandCursor)  
        solve_kp_btn.setStyleSheet(
             "QPushButton {"
            "   font-size: 17px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size:18px;"
            "}"
        )
        solve_kp_btn.clicked.connect(self.solve_knapsack)
        result_layout.addWidget(solve_kp_btn)

        # Result
        self.outputArea = QTextEdit()
        self.outputArea.setReadOnly(True)
        result_layout.addWidget(self.outputArea)
        result_layout.addWidget(back_button)
        result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.setContentsMargins(0, 50, 0, 0)
        main_layout.addLayout(back_layout)
        main_layout.setSpacing(10)
        main_layout.addLayout(input_layout)

        main_layout.addLayout(result_layout)
        # Set Layout
        self.setLayout(main_layout)

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
