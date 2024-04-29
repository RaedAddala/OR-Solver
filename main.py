import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from HomePage import HomePage
from KnapsackSolver import KnapsackSolver
from TransportationSolver import TransportationSolver

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operations Research Project")
        self.setGeometry(200, 100, 1200, 800)

        self.stack = QStackedWidget(self)

        self.home_page = HomePage(self)
        self.knapsack_solver = KnapsackSolver(self)
        self.transportation_solver = TransportationSolver(self)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.knapsack_solver)
        self.stack.addWidget(self.transportation_solver)

        self.setCentralWidget(self.stack)

    def show_page(self, page_name):
        if page_name == "Home":
            self.stack.setCurrentIndex(0)
        elif page_name == "Knapsack":
            self.stack.setCurrentIndex(1)
        elif page_name == "Transportation":
            self.stack.setCurrentIndex(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())