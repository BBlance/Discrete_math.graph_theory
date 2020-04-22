import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from MainWindow import Ui_MainWindow


class TestWidget(QMainWindow):
    def __init__(self):
        super(TestWidget, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TestWidget()
    form.show()
    sys.exit(app.exec_())
