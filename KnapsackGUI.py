from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QMessageBox
from gurobipy import Model, GRB
from PyQt5.QtCore import Qt

class KnapsackGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Styling
        self.setStyleSheet("font-size: 16px;")
        # Layouts
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.input_attributes_layout = QVBoxLayout()
        self.input_constraints_layout = QVBoxLayout()
        self.input_constraints_row=QHBoxLayout()
        self.layout.addLayout(self.input_attributes_layout)
        self.layout.addLayout(self.input_constraints_layout)
 

        
        
    
        # Back Button
        back_button = QPushButton("Back gui")
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
        self.layout.addWidget(back_button)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        #nbr of attributes input ------------------------------------------------------------------------------
        self.attribute_number_input = QLineEdit("2")
        self.layout.addWidget(QLabel("attributes number:"))
        self.layout.addWidget(self.attribute_number_input)
        print(self.attribute_number_input.text())
        self.user_attributes_inputs = ["" for _ in range(int(self.attribute_number_input.text()))]
        self.attribute_number_input.textChanged.connect(self.update_matrix)


        
        set_attributes_button = QPushButton("set")
        set_attributes_button.clicked.connect(self.print_attribues)
        self.layout.addWidget(set_attributes_button)
        
        
        self.constraints_number_input = QLineEdit("1")
        self.layout.addWidget(QLabel("constraints number:"))
        self.layout.addWidget(self.constraints_number_input)
        self.constraints_number_input.textChanged.connect(self.update_matrix)
        self.user_constraints_inputs = [["" for _ in range(int(self.constraints_number_input.text()))] for _ in range(int(self.attribute_number_input.text()))]



        set_constraints_button = QPushButton("set constraints")
        set_constraints_button.clicked.connect(self.print_constraints)
        self.layout.addWidget(set_constraints_button)
        
    #nbr of attributes input ------------------------------------------------------------------------------


        # Input
        self.capacity_input = QLineEdit("7")
        self.weights_input = QLineEdit("2,5,4,3")
        self.values_input = QLineEdit("20,30,40,50")

        self.capacity_input.setStyleSheet(
           "QLineEdit {"
            "   padding: 7px;"
            "   border: 3px solid #A1D1E9;"
            "   border-radius: 10px;"
            "   font-size: 16px;"
            "}"
        )

        self.weights_input.setStyleSheet(
            "QLineEdit {"
            "   padding: 7px;"
            "   border: 3px solid #A1D1E9;"
            "   border-radius: 10px;"
            "   font-size: 16px;"
            "}"
        )

        self.values_input.setStyleSheet(
            "QLineEdit {"
            "   padding: 7px;"
            "   border: 3px solid #A1D1E9;"
            "   border-radius: 10px;"
            "   font-size: 16px;"
            "}"
        )
        self.layout.setContentsMargins(0, 20, 0, 0)
        self.layout.addWidget(QLabel("Knapsack Capacity (kg):"))
        self.layout.addWidget(self.capacity_input)
        self.layout.addWidget(QLabel("Item Values (comma-separated):"))
        self.layout.addWidget(self.values_input)
        self.layout.addWidget(QLabel("Item Weights (comma-separated):"))
        self.layout.addWidget(self.weights_input)

        # Solve
        solve_kp_btn = QPushButton('Solve Knapsack', self)
        solve_kp_btn.setFixedSize(250, 50)
        solve_kp_btn.setCursor(Qt.PointingHandCursor)  
        solve_kp_btn.setStyleSheet(
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
        solve_kp_btn.clicked.connect(self.solve_knapsack)
        self.layout.addWidget(solve_kp_btn)

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
        self.layout.addWidget(reset_btn)



        # Result
        self.outputArea = QTextEdit()
        self.outputArea.setStyleSheet(
            "QTextEdit {"
            "   padding: 5px;"
            "   border: 2px solid #A1D1E9;"
            "   border-radius: 8px;"
            "   font-size: 16px;"
            "}"
        )
        self.outputArea.setReadOnly(True)
        self.layout.addWidget(self.outputArea)
        self.layout.addWidget(back_button)
        #self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 30, 0, 0)

      #-----------------------------------constraints
              
    def print_constraints(self):
        print(self.constraints_number_input.text())
                #num_attributes = int(attributes_text) if attributes_text else 0

        n_constraints= int(self.constraints_number_input.text()) if self.constraints_number_input.text() else 0
        n_attributes= int(self.attribute_number_input.text()) if self.attribute_number_input.text() else 0

        #delete old inputs
        
        for i in reversed(range(self.input_constraints_layout.count())):
            widget = self.input_constraints_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()


        #set inputs
        for i in range(n_attributes):
            label_attribute = QLabel(f"attribute  {i+1}:", self)
            #const_inputs = []  # List to store inputs for each row
            self.input_constraints_layout.addWidget(label_attribute)      

            for j in range(n_constraints):
                label = QLabel(f"constraint  {j+1}:", self)
                constraint_value = QLineEdit(self)
                self.input_constraints_layout.addWidget(label)      
                self.input_constraints_layout.addWidget(constraint_value)
                #self.user_constraints_inputs[i][j]=constraint_value
                #☻const_inputs.append(constraint_value)
                self.user_constraints_inputs[i][j]=constraint_value    
                constraint_value.textChanged.connect(lambda text, i=i, j=j: self.update_constraint_value(text, i, j))

        set_constraints_button = QPushButton("set const")
        self.input_constraints_layout.addWidget(set_constraints_button)
        set_constraints_button.clicked.connect(self.print_constraints_values)  
        
            
    def print_constraints_values(self): #just to test 
        print("user_const_inputs: ",self.user_constraints_inputs) 
        
        
         
    def update_constraint_value(self, text, row, col):
        self.user_constraints_inputs[row][col] = text
        print("user_const_inputs: ",self.user_constraints_inputs) 


        

      
      
      
      
      
      
      
      
      
      # -----------------------------------attributes
        
    def print_attribues(self):
        print(self.attribute_number_input.text())
        n= int(self.attribute_number_input.text())
        self.user_attributes_inputs = []

        #delete old inputs
        for i in reversed(range(self.input_attributes_layout.count())):
            widget = self.input_attributes_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        #set inputs
        for i in range(n):
            label = QLabel(f"Attribute {i+1}:", self)
            attribute_value = QLineEdit(self)
            self.input_attributes_layout.addWidget(label)      
            self.input_attributes_layout.addWidget(attribute_value)
            self.user_attributes_inputs.append(attribute_value)
            
            #set button
        set_attributes_button = QPushButton("set attributes")
        self.input_attributes_layout.addWidget(set_attributes_button)
        set_attributes_button.clicked.connect(self.print_attribue_values)  
        
            
    def print_attribue_values(self): #♥just to test 
        self.update_user_attributes_inputs()
        print("user_inputs",self.user_attributes_inputs)    
        
    def update_user_attributes_inputs(self):
        self.user_attributes_inputs.clear()
        for i in range(self.input_attributes_layout.count()):
            widget = self.input_attributes_layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                self.user_attributes_inputs.append(widget.text()) 


#________________________________________________________________________



    def update_matrix(self):
           
        attributes_text = self.attribute_number_input.text()
        constraints_text = self.constraints_number_input.text()

        # Check if the input is not empty before converting to integer
        num_attributes = int(attributes_text) if attributes_text else 0
        num_constraints = int(constraints_text) if constraints_text else 0

        self.user_attributes_inputs = [""] * num_attributes

            # Update user_attributes_inputs based on new number of attributes
            #self.user_attributes_inputs = [""] * num_attributes

            # Update user_constraints_inputs based on new number of attributes and constraints
        self.user_constraints_inputs = [["" for _ in range(num_constraints)] for _ in range(num_attributes)]
        self.print_constraints()

















    def gotoHome(self):
        self.parent.stack.setCurrentIndex(0)

    def reset_data(self):
        self.capacity_input.clear()
        self.weights_input.clear()
        self.values_input.clear()
        self.outputArea.clear()

    

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
