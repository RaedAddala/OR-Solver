import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QFont, QIcon
from HomePage import HomePage
from SelectionPrblmUI import SelectionPrblmUI
from TransportationSolver import TransportationSolver

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operations Research Project")
        self.setGeometry(330, 120, 1200, 800)
        self.setStyleSheet("QMainWindow { background-color: #E1EFF3; }")
        self.stack = QStackedWidget(self)
        self.home_page = HomePage(self)
        self.selectionProblem = SelectionPrblmUI(self)
        self.transportation_solver = TransportationSolver(self)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.selectionProblem)
        self.stack.addWidget(self.transportation_solver)
        self.setCentralWidget(self.stack)

    def show_page(self, page_name):
        if page_name == "Home":
            self.stack.setCurrentIndex(0)
        elif page_name == "Selection":
            self.stack.setCurrentIndex(1)
        elif page_name == "Transportation":
            self.stack.setCurrentIndex(2)

    # def getSelectionProblem(self):
    #     return self.selectionProblem

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())