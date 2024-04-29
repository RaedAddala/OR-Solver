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
        inputLayout = QHBoxLayout()
        # back button
        back_button = QPushButton('Back to Home')
        back_button.clicked.connect(self.gotoHome)
        layout.addWidget(back_button)

        # Labels and input fields
        valuesLabel = QLabel("Values:")
        self.valuesInput = QLineEdit("20,30,40,50")
        weightsLabel = QLabel("Weights:")
        self.weightsInput = QLineEdit("2,5,4,3")
        capacityLabel = QLabel("Capacity:")
        self.capacityInput = QLineEdit("7")

        # Organize inputs horizontally
        inputLayout.addWidget(valuesLabel)
        inputLayout.addWidget(self.valuesInput)
        inputLayout.addWidget(weightsLabel)
        inputLayout.addWidget(self.weightsInput)
        inputLayout.addWidget(capacityLabel)
        inputLayout.addWidget(self.capacityInput)
        
        # Solve button
        solveButton = QPushButton("Solve Knapsack")
        solveButton.clicked.connect(self.solve_knapsack)
        
        # Output text area
        self.outputArea = QTextEdit()
        self.outputArea.setReadOnly(True)

        # Add widgets to layout
        layout.addLayout(inputLayout)
        layout.addWidget(solveButton)
        layout.addWidget(self.outputArea)
        
        # Set layout
        self.setLayout(layout)
   
    def gotoHome(self):
        self.parent.stack.setCurrentIndex(0)

    def solve_knapsack(self):
        try:
            values = list(map(int, self.valuesInput.text().split(',')))
            weights = list(map(int, self.weightsInput.text().split(',')))
            capacity = int(self.capacityInput.text())
            n = len(values)

            m = Model("knapsack")
            x = m.addVars(n, vtype=GRB.BINARY, name="x")
            m.setObjective(sum(values[i] * x[i] for i in range(n)), GRB.MAXIMIZE)
            m.addConstr(sum(weights[i] * x[i] for i in range(n)) <= capacity, "capacity")
            m.optimize()

            if m.status == GRB.OPTIMAL:
                result = f"Optimal value: {m.objVal}\nSelected items:\n"
                for i in range(n):
                    if x[i].X > 0.5:  # If x[i] is 1
                        result += f"Item {i} - Value: {values[i]}, Weight: {weights[i]}\n"
                self.outputArea.setText(result)
            else:
                self.outputArea.setText("No optimal solution found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", "Failed to solve the problem: " + str(e))
