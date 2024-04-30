from PyQt5.QtWidgets import QWidget,QHBoxLayout, QPushButton, QVBoxLayout,QLabel
from PyQt5.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        title_layout = QVBoxLayout()
        description_layout = QVBoxLayout()
        problems_layout = QHBoxLayout()
        title_label = QLabel("HOME PAGE")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight:light; font-size: 15px;  color: #555555;  ")  # Added margin-bottom

        welcome_label = QLabel("- Welcome to our Operational Research project -")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet(" font-size: 28px; font-weight:bold;color:#2980b9 ") 


        description_label = QLabel("where we tackle optimization challenges in both Knapsack and Transportation problems to enhance \n decision-making and resource allocation efficiency.")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("font-weight:semi-weight; font-size: 24px;  ") 





        btn_knapsack = QPushButton('Knapsack Problem')
        btn_knapsack.setFixedSize(300, 70)
        btn_knapsack.setCursor(Qt.PointingHandCursor)  
        btn_knapsack.setStyleSheet(
             "QPushButton {"
            "   font-size: 19px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size:21px;"
            "}"
        )
        btn_knapsack.clicked.connect(lambda: self.parent.show_page("Knapsack"))
        
        btn_transportation = QPushButton('Transportation Problem')
        btn_transportation.setFixedSize(300, 70)
        btn_transportation.setCursor(Qt.PointingHandCursor)  
        btn_transportation.setStyleSheet(
            "QPushButton {"
            "   font-size: 19px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size: 21px;"
            "}"
        )
        btn_transportation.clicked.connect(lambda: self.parent.show_page("Transportation"))
      
        title_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignTop)  # Align the title_label to the top
        description_layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignTop)
        description_layout.addWidget(description_label, alignment=Qt.AlignmentFlag.AlignTop)
        problems_layout.addWidget(btn_knapsack)
        problems_layout.addWidget(btn_transportation)
        problems_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(description_layout)
        main_layout.addLayout(problems_layout)
        description_layout.setContentsMargins(50, 0, 50, 50)  # Adjust the top and bottom margins of main_layout

        main_layout.setContentsMargins(50, 0, 50, 50)  # Adjust the top and bottom margins of main_layout

        self.setLayout(main_layout)


