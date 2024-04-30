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
        problems_layout = QHBoxLayout()
        title_label = QLabel("HOME PAGE")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight: semi-bold; font-size: 24px; ")  # Added margin-bottom


        description_label = QLabel("Welcome to our Operational Research project,\nwhere we tackle optimization challenges in both Knapsack and Transportation problems to enhance decision-making and resource allocation efficiency.")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet(" font-size: 18px; color: #555555; ") 





        btn_knapsack = QPushButton('Knapsack Problem')
        btn_knapsack.setFixedSize(200, 50)
        btn_knapsack.setCursor(Qt.PointingHandCursor)  
        btn_knapsack.setStyleSheet(
             "QPushButton {"
            "   font-size: 16px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "   transition: background-color 0.3s, width 0.3s, height 0.3s, box-shadow 0.3s;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size: 17px;"
            "   width: 220px !important;"
            "   height: 60px;"
            "   box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3) !important ;"
            "}"
        )
        btn_knapsack.clicked.connect(lambda: self.parent.show_page("Knapsack"))
        
        btn_transportation = QPushButton('Transportation Problem')
        btn_transportation.setFixedSize(200, 50)
        btn_transportation.setCursor(Qt.PointingHandCursor)  
        btn_transportation.setStyleSheet(
            "QPushButton {"
            "   font-size: 16px;"
            "   border-radius: 10px;"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "   transition: background-color 0.3s, width 0.3s, height 0.3s, box-shadow 0.3s;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "   font-size: 17px;"
            "   width: 220px !important;"
            "   height: 60px;"
            "   box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3) !important ;"
            "}"
        )
        btn_transportation.clicked.connect(lambda: self.parent.show_page("Transportation"))
      
        title_layout.addWidget(title_label)
        title_layout.addWidget(description_label)
        problems_layout.addWidget(btn_knapsack)
        problems_layout.addWidget(btn_transportation)
        problems_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(problems_layout)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.setContentsMargins(50, 50, 50, 50)
        title_layout.setSpacing(100)
        main_layout.setSpacing(10)

        self.setLayout(main_layout)


