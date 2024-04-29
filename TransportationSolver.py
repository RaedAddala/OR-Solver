from PyQt5.QtWidgets import ( QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QMessageBox)
from PyQt5.QtGui import QFont
from gurobipy import Model, GRB

class TransportationSolver(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
       # Styling
        self.setStyleSheet("font-size: 14px;")
        
        # Layout
        layout = QVBoxLayout()

        # Instruction label
        instruction_label = QLabel('Enter supply, demand, and cost data:')
        instruction_label.setFont(QFont('Arial', 12))
        layout.addWidget(instruction_label)

        # Supply input
        self.supply_input = QLineEdit()
        self.supply_input.setPlaceholderText('Enter supplies separated by commas, e.g., 20,30,25')
        layout.addWidget(self.supply_input)

        # Demand input
        self.demand_input = QLineEdit()
        self.demand_input.setPlaceholderText('Enter demands separated by commas, e.g., 10,30,35')
        layout.addWidget(self.demand_input)

        # Cost input
        self.cost_input = QLineEdit()
        self.cost_input.setPlaceholderText('Enter costs in matrix form, e.g., 8,6,10;9,7,4;3,4,2')
        layout.addWidget(self.cost_input)

        # Solve button
        solve_button = QPushButton('Solve')
        solve_button.setFont(QFont('Arial', 12))
        solve_button.setStyleSheet("QPushButton {background-color: #007BFF; color: white; border-radius: 8px; padding: 10px;}")
        solve_button.clicked.connect(self.solve_transportation)
        layout.addWidget(solve_button)

        # Output Text Area
        self.output_text_area = QTextEdit()
        self.output_text_area.setReadOnly(True)
        layout.addWidget(self.output_text_area)

        self.setLayout(layout)

    def solve_transportation(self):
        try:
            supply = list(map(int, self.supply_input.text().split(',')))
            demand = list(map(int, self.demand_input.text().split(',')))
            cost = {}
            cost_rows = self.cost_input.text().split(';')
            for i, row in enumerate(cost_rows):
                costs = list(map(int, row.split(',')))
                for j, c in enumerate(costs):
                    cost[(i, j)] = c

            # Create and solve the model
            model = Model("Transportation")
            num_sources = len(supply)
            num_destinations = len(demand)
            x = model.addVars(num_sources, num_destinations, obj=cost, name="x", vtype=GRB.CONTINUOUS)
            model.modelSense = GRB.MINIMIZE

            for i in range(num_sources):
                model.addConstr(sum(x[i, j] for j in range(num_destinations)) <= supply[i], f"supply_{i}")

            for j in range(num_destinations):
                model.addConstr(sum(x[i, j] for i in range(num_sources)) >= demand[j], f"demand_{j}")

            model.optimize()

            # Display results
            if model.status == GRB.OPTIMAL:
                result_text = f"Optimal Cost: {model.objVal}\n"
                for i in range(num_sources):
                    for j in range(num_destinations):
                        if x[i, j].X > 0.001:
                            result_text += f"Ship {x[i, j].X:.2f} units from Source {i} to Destination {j}\n"
                self.output_text_area.setText(result_text)
            else:
                self.output_text_area.setText("No feasible solution found.")
        except Exception as e:
            QMessageBox.critical(self, "Input Error", str(e), QMessageBox.Ok)

