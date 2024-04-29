from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

class TransportationSolver(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        backButton = QPushButton("Back to Home")
        backButton.clicked.connect(lambda: self.parent.show_page("Home"))
        layout.addWidget(backButton)
        self.setLayout(layout)
