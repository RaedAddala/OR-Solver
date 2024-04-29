from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        title = QPushButton("Home")
        title.setEnabled(False)  # Make it look like a title, not clickable
        
        btn_knapsack = QPushButton('Knapsack Problem')
        btn_knapsack.clicked.connect(lambda: self.parent.show_page("Knapsack"))
        
        btn_transportation = QPushButton('Transportation Problem')
        btn_transportation.clicked.connect(lambda: self.parent.show_page("Transportation"))
        
        layout.addWidget(title)
        layout.addWidget(btn_knapsack)
        layout.addWidget(btn_transportation)
        
        self.setLayout(layout)
