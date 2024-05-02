from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLabel,QHBoxLayout, QLineEdit, QTextEdit, QMessageBox)
from gurobipy import Model, GRB
from PyQt5.QtCore import Qt

class TransportationSolver(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Styling
        self.setStyleSheet("font-size: 16px;")
        # Main Layout
        back_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        main_layout = QVBoxLayout()
        result_layout = QVBoxLayout()   
        buttons_layout = QHBoxLayout()
        # back button
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
        main_layout.addLayout(back_layout)

        # Instructions
        instruction_label = QLabel("Enter supply, demand, and cost matrix (comma-separated; rows separated by semicolons):")
        # Supply Input
        supply_label = QLabel("Supply:")
        self.supply_input = QLineEdit("20,30,25")
        self.supply_input.setStyleSheet(
            "QLineEdit {"
            "   padding: 5px;"
            "   border: 3px solid #A1D1E9;"
            "   border-radius: 10px;"
            "   font-size: 16px;"
            "}"
        )
        # Demand Input
        demand_label = QLabel("Demand:")
        self.demand_input = QLineEdit("10,30,35")
        self.demand_input.setStyleSheet(
            "QLineEdit {"
            "   padding: 5px;"
            "   border: 3px solid #A1D1E9;"
            "   border-radius: 10px;"
            "   font-size: 16px;"
            "}"
        )
        # Cost Input
        cost_label = QLabel("Cost Matrix:")
        self.cost_input = QLineEdit("1,1,10;0,2,4;1,2,2;")
        self.cost_input.setStyleSheet(
            "QLineEdit {"
            "   padding: 5px;"
            "   border: 3px solid #A1D1E9;"
            "   border-radius: 10px;"
            "   font-size: 16px;"
            "}"
        )
        
        input_layout.setContentsMargins(0, 30, 0, 0)
        input_layout.addWidget(instruction_label)
        input_layout.addWidget(supply_label)
        input_layout.addWidget(self.supply_input)
        input_layout.addWidget(demand_label)
        input_layout.addWidget(self.demand_input)
        input_layout.addWidget(cost_label)
        input_layout.addWidget(self.cost_input)

        main_layout.addLayout(input_layout)

        # Solve Button
        solve_button = QPushButton("Solve Transportation Problem",self)
        solve_button.setFixedSize(250, 50)
        solve_button.setCursor(Qt.PointingHandCursor)  
        solve_button.setStyleSheet(
             "QPushButton {"
            "   font-size: 17px;"
            "   border-radius: 13px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size:18px;"
            "}"
        )
        solve_button.clicked.connect(self.solve_transportation)
        buttons_layout.addWidget(solve_button)




 #reset
        reset_btn = QPushButton('reset data', self)
        reset_btn.setFixedSize(250, 50)
        reset_btn.setCursor(Qt.PointingHandCursor)  
        reset_btn.setStyleSheet(
             "QPushButton {"
            "   font-size: 17px;"
            "   border-radius: 13px;"
            "   background-color: #C8CECF;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #BABFC0;"
            "   font-size:18px;"
            "}"
        )
        reset_btn.clicked.connect(self.reset_data)
        buttons_layout.addWidget(reset_btn)
        result_layout.addLayout(buttons_layout)







        # Output Text Area
        self.output_area = QTextEdit()
        self.output_area.setStyleSheet(
            "QTextEdit {"
            "   padding: 5px;"
            "   border: 2px solid #A1D1E9;"
            "   border-radius: 8px;"
            "   font-size: 16px;"
            "}"
        )
        self.output_area.setReadOnly(True)
        result_layout.addWidget(self.output_area)
        result_layout.setContentsMargins(0, 30, 0, 0)

        # Set Layout
        main_layout.addLayout(result_layout)
        main_layout.setSpacing(10)

        self.setLayout(main_layout)
    
    def gotoHome(self):
        self.parent.stack.setCurrentIndex(0)
    def solve_transportation(self):
        try:
            supply = list(map(int, self.supply_input.text().split(',')))
            demand = list(map(int, self.demand_input.text().split(',')))
            if not (all_positive(supply)):
                raise InvalidInputError("Supply Capacities must be all positive")
            if not (all_positive(demand)):
                raise InvalidInputError("Demand Capacities must be all positive")
            cost_dict = {}
            cost_rows = self.cost_input.text().strip().split(';')
            if not (cost_rows[-1]):
                cost_rows = cost_rows[1:-2]
            for i, row in enumerate(cost_rows):
                costs = list(map(int, row.split(',')))
                if not (all_positive(costs)):
                    raise InvalidInputError("costs Capacities must be all positive")
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
        
        except InvalidInputError as e:
            QMessageBox.critical(self, "Invalid Input Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Input Error", "Failed to solve the problem: " + str(e))

    def reset_data(self):
            self.cost_input.clear()
            self.supply_input.clear()
            self.demand_input.clear()
            self.output_area.clear()

class InvalidInputError(Exception):
    pass

all_positive = lambda lst: all(value >= 0 for value in lst)