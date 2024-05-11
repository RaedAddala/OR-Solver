import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QFont, QIcon
from HomePage import HomePage
from KnapsackGUI import KnapsackGUI
from TransportationSolver import TransportationSolver

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operations Research Project")
        self.setGeometry(330, 120, 1200, 800)
        self.setStyleSheet("QMainWindow { background-color: #E1EFF3; }")
        self.stack = QStackedWidget(self)
        self.home_page = HomePage(self)
        self.knapsack_solver = KnapsackGUI(self)
        self.transportation_solver = TransportationSolver(self)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.knapsack_solver)
        self.stack.addWidget(self.transportation_solver)
        self.setCentralWidget(self.stack)

    def show_page(self, page_name):
        if page_name == "Home":
            self.stack.setCurrentIndex(0)
        elif page_name == "KnapsackGUI":
            self.stack.setCurrentIndex(1)
        elif page_name == "Transportation":
            self.stack.setCurrentIndex(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())