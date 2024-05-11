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
        self.back_layout = QVBoxLayout()
        self.input_layout=QVBoxLayout()
        self.input_numbers_layout = QHBoxLayout()
        self.input_attributes_values_layout = QHBoxLayout()
        self.input_constraints_names_layout = QHBoxLayout()
        self.input_constraints_values_layout = QVBoxLayout()
        self.input_limits_layout = QHBoxLayout()    
        self.result_layout = QVBoxLayout()

        self.input_layout.addLayout(self.input_numbers_layout)
        self.input_layout.addLayout(self.input_attributes_values_layout)
        self.input_layout.addLayout(self.input_constraints_names_layout)
        self.input_layout.addLayout(self.input_constraints_values_layout)
        self.input_layout.addLayout(self.input_limits_layout)
        
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.result_layout)
        self.layout.addLayout(self.back_layout)

        self.setLayout(self.layout)


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
        self.back_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        back_button.clicked.connect(self.gotoHome)
        self.back_layout.addWidget(back_button)
        
        
        #nbr of attributes input ------------------------------------------------------------------------------
        self.attribute_number_input = QLineEdit("2")
        self.attribute_number_input.setStyleSheet(
           "QLineEdit {"
            "   padding: 7px;"
            "   border: 3px solid #A1D1E9;"
            "   border-radius: 10px;"
            "   font-size: 16px;"
            "}"
        )
        self.input_numbers_layout.addWidget(QLabel("attributes number:"))
        self.input_numbers_layout.addWidget(self.attribute_number_input)
        print(self.attribute_number_input.text())
        self.user_attributes_inputs = ["" for _ in range(int(self.attribute_number_input.text()))]

        
        self.constraints_number_input = QLineEdit("3")
        self.constraints_number_input.setStyleSheet(
           "QLineEdit {"
            "   padding: 7px;"
            "   border: 3px solid #A1D1E9;"
            "   border-radius: 10px;"
            "   font-size: 16px;"
            "}"
        )
        
        self.input_numbers_layout.addWidget(QLabel("constraints number:"))
        self.input_numbers_layout.addWidget(self.constraints_number_input)
        self.user_constraints_inputs = [["" for _ in range(int(self.constraints_number_input.text()))] for _ in range(int(self.attribute_number_input.text()))]
        self.user_constraints_names= [""] * int(self.constraints_number_input.text())
        
        set_attributes_button = QPushButton("set input")
        set_attributes_button.setFixedSize(230, 30)
        set_attributes_button.setCursor(Qt.PointingHandCursor)  
        set_attributes_button.setStyleSheet(
             "QPushButton {"
            "   font-size: 14px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size:15px;"
            "}"
        )
        set_attributes_button.clicked.connect(self.set_input)
        self.input_numbers_layout.addWidget(set_attributes_button)

      
# -----------------------------------set   attributes   values
        
    def print_attribues(self):
        print(self.attribute_number_input.text())
        n= int(self.attribute_number_input.text())

        #delete old inputs
        for i in reversed(range(self.input_attributes_values_layout.count())):
            widget = self.input_attributes_values_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        #set inputs
        for i in range(n):
            label = QLabel(f"Attribute {i+1}:", self)
            attribute_value = QLineEdit(self)
            attribute_value.setStyleSheet(
                "QLineEdit {"
                    "   padding: 7px;"
                    "   border: 3px solid #A1D1E9;"
                    "   border-radius: 10px;"
                    "   font-size: 16px;"
                    "}"
                )
            self.input_attributes_values_layout.addWidget(label)      
            self.input_attributes_values_layout.addWidget(attribute_value)
            self.user_attributes_inputs.append(attribute_value)          
            #set button
        set_attributes_button = QPushButton("set attributes values")
        set_attributes_button.setFixedSize(230, 30)
        set_attributes_button.setCursor(Qt.PointingHandCursor)  
        set_attributes_button.setStyleSheet(
             "QPushButton {"
            "   font-size: 14px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "   font-style: italic;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size:15px;"
            "}"
        )        
        self.input_attributes_values_layout.addWidget(set_attributes_button)
        set_attributes_button.clicked.connect(self.set_attribue_values)  
        
            
    def set_attribue_values(self): #♥just to test 
        self.update_user_attributes_inputs()
        self.set_constraints()
 
        
    def update_user_attributes_inputs(self):
        self.user_attributes_inputs.clear()
        for i in range(self.input_attributes_values_layout.count()):
            widget = self.input_attributes_values_layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                self.user_attributes_inputs.append(widget.text()) 



        #☻----------------------------------------------------constarints names set:
             
        
    def set_constraints(self):
        n= int(self.constraints_number_input.text())
        #delete old inputs
        for i in reversed(range(self.input_constraints_names_layout.count())):
            widget = self.input_constraints_names_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        #set inputs
        for i in range(n):
            label = QLabel(f"constraint {i+1}:", self)
            constraint_name = QLineEdit(self)
            constraint_name.setStyleSheet(
           "QLineEdit {"
            "   padding: 5px;"
            "   border: 2px solid #A1D1E9;"
            "   border-radius: 10px;"
            "   font-size: 16px;"
            "}"
        )
            self.input_constraints_names_layout.addWidget(label)      
            self.input_constraints_names_layout.addWidget(constraint_name)
            self.user_constraints_names.append(constraint_name)  
            #set button
        set_constraint_names_button = QPushButton("set constraint names")
        set_constraint_names_button.setFixedSize(230, 30)
        set_constraint_names_button.setCursor(Qt.PointingHandCursor)  
        set_constraint_names_button.setStyleSheet(
             "QPushButton {"
            "   font-size: 14px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size:15px;"
            "}"
        )
        self.back_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_constraints_names_layout.addWidget(set_constraint_names_button)
        set_constraint_names_button.clicked.connect(self.set_constraint_names_values)  
        
            
    def set_constraint_names_values(self): 
        self.update_constraint_names()
        self.print_constraints()
 
        
    def update_constraint_names(self):
        self.user_constraints_names.clear()
        for i in range(self.input_constraints_names_layout.count()):
            widget = self.input_constraints_names_layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                self.user_constraints_names.append(widget.text()) 



      #-----------------------------------set constraints values
              
    def print_constraints(self):
        n_constraints= int(self.constraints_number_input.text()) if self.constraints_number_input.text() else 0
        n_attributes= int(self.attribute_number_input.text()) if self.attribute_number_input.text() else 0
        print("n_constraints",n_constraints,"n_attributes",n_attributes)
        #delete old inputs    
        for i in reversed(range(self.input_constraints_values_layout.count())):
            widget = self.input_constraints_values_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        #set inputs
        for i in range(n_attributes):
            label_attribute = QLabel(f"attribute  {i+1}:", self)
            if self.user_attributes_inputs[i] != "":
                label_attribute.setText(self.user_attributes_inputs[i])          
            self.input_constraints_values_layout.addWidget(label_attribute)      
            for j in range(n_constraints):
                label = QLabel(f"constraint  {j+1}:", self)
                if self.user_constraints_names[j] != "":
                    label.setText(self.user_constraints_names[j])
                constraint_value = QLineEdit(self)
                constraint_value.setStyleSheet(
                    "QLineEdit {"
                        "   padding: 5px;"
                        "   border: 2px solid #A1D1E9;"
                        "   border-radius: 14px;"
                        "   font-size: 15px;"
                        "}"
                    )
                self.input_constraints_values_layout.addWidget(label)      
                self.input_constraints_values_layout.addWidget(constraint_value)

                self.user_constraints_inputs[i][j]=constraint_value    
                constraint_value.textChanged.connect(lambda text, i=i, j=j: self.update_constraint_value(text, i, j))

        set_constraints_button = QPushButton("set constraints")
        set_constraints_button.setFixedSize(230, 30)
        set_constraints_button.setCursor(Qt.PointingHandCursor)  
        set_constraints_button.setStyleSheet(
             "QPushButton {"
            "   font-size: 14px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size:15px;"
            "}"
        )        
        self.input_constraints_values_layout.addWidget(set_constraints_button)
       # set_constraints_button.clicked.connect(self.solve_knapsack)  

        
         
    def update_constraint_value(self, text, row, col):
        self.user_constraints_inputs[row][col] = text

      
      
      
      
    

#________________________________________________________________________



    # def update_matrix(self):
    #     self.input_constraints_number_layout=QLineEdit("1")
    #     attributes_text = self.attribute_number_input.text()  if self.attribute_number_input.text() else ""
        
    #     #♦constraints_text = self.constraints_number_input.text() if self.constraints_number_input else ""
    #     if self.constraints_number_input:
    #         if self.constraints_number_input.text():
    #             constraints_text = self.constraints_number_input.text()
    #         else:
    #             constraints_text = ""
    #     else:
    #         constraints_text = ""            

    #     # Check if the input is not empty before converting to integer
    #     num_attributes = int(attributes_text) if attributes_text else 0
    #     num_constraints = int(constraints_text) if constraints_text else 0

    #     self.user_attributes_inputs = [""] * num_attributes

    #         # Update user_attributes_inputs based on new number of attributes
    #         #self.user_attributes_inputs = [""] * num_attributes

    #         # Update user_constraints_inputs based on new number of attributes and constraints
    #     self.user_constraints_inputs = [["" for _ in range(num_constraints)] for _ in range(num_attributes)]
    #     self.print_constraints()





#_______________________________________________set input:
    def set_input(self):
        self.user_constraints_inputs = [["" for _ in range(int(self.constraints_number_input.text()))] for _ in range(int(self.attribute_number_input.text()))]
        self.user_constraints_names= [""] * int(self.constraints_number_input.text())
        self.user_attributes_inputs = ["" for _ in range(int(self.attribute_number_input.text()))]
        self.print_attribues()











    def gotoHome(self):
        self.parent.stack.setCurrentIndex(0)

    def reset_data(self):
        self.attribute_number_input.clear()
        self.constraints_number_input.clear()


    

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
