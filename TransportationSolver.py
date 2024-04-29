from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QMessageBox)
from gurobipy import Model, GRB

class TransportationSolver(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Styling
        self.setStyleSheet("font-size: 14px;")
        # Main Layout
        layout = QVBoxLayout()
        # back button
        back_button = QPushButton('Back to Home')
        back_button.clicked.connect(self.gotoHome)
        layout.addWidget(back_button)
        # Instructions
        instruction_label = QLabel("Enter supply, demand, and cost matrix (comma-separated; rows separated by semicolons):")
        layout.addWidget(instruction_label)
        # Supply Input
        supply_label = QLabel("Supply:")
        self.supply_input = QLineEdit("20,30,25")
        layout.addWidget(supply_label)
        layout.addWidget(self.supply_input)
        # Demand Input
        demand_label = QLabel("Demand:")
        self.demand_input = QLineEdit("10,30,35")
        layout.addWidget(demand_label)
        layout.addWidget(self.demand_input)
        # Cost Input
        cost_label = QLabel("Cost Matrix:")
        self.cost_input = QLineEdit("0,1,10;0,2,4;1,2,2;...")
        layout.addWidget(cost_label)
        layout.addWidget(self.cost_input)
        # Solve Button
        solve_button = QPushButton("Solve Transportation Problem")
        solve_button.clicked.connect(self.solve_transportation)
        layout.addWidget(solve_button)

        # Output Text Area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        # Set Layout
        self.setLayout(layout)
    
    def gotoHome(self):
        self.parent.stack.setCurrentIndex(0)
    def solve_transportation(self):
        try:
            supply = list(map(int, self.supply_input.text().split(',')))
            demand = list(map(int, self.demand_input.text().split(',')))
            cost_dict = {}
            cost_rows = self.cost_input.text().split(';')
            for i, row in enumerate(cost_rows):
                costs = list(map(int, row.split(',')))
                for j, cost in enumerate(costs):
                    cost_dict[(i, j)] = cost

            # Gurobi Solver Integration
            model = Model("Transportation")
            num_sources = len(supply)
            num_destinations = len(demand)
            x = model.addVars(num_sources, num_destinations, obj=cost_dict, name="x", vtype=GRB.CONTINUOUS)
            model.modelSense = GRB.MINIMIZE

            for i in range(num_sources):
                model.addConstr(sum(x[i, j] for j in range(num_destinations)) <= supply[i], f"supply_{i}")

            for j in range(num_destinations):
                model.addConstr(sum(x[i, j] for i in range(num_sources)) >= demand[j], f"demand_{j}")

            model.optimize()

            if model.status == GRB.OPTIMAL:
                result = f"Optimal Cost: {model.objVal}\n"
                for i in range(num_sources):
                    for j in range(num_destinations):
                        if x[i, j].X > 0.001:
                            result += f"Ship {x[i, j].X:.2f} units from Source {i} to Destination {j}\n"
                self.output_area.setText(result)
            else:
                self.output_area.setText("No feasible solution found.")
        except Exception as e:
            QMessageBox.critical(self, "Input Error", "Failed to solve the problem: " + str(e))
