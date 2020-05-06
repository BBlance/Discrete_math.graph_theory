import sys

from PySide2.QtCore import Slot, Qt, QSize
from PySide2.QtGui import QPainter, QPen, QColor, QIcon
from PySide2.QtWidgets import QDialog, QWidget, QApplication, QComboBox

from ui_ThicknessDialog import Ui_ThicknessDialog


class ThicknessDialog(QDialog):

    def __init__(self, parent=None, str="Dialogs", thickness=3, penStyle=Qt.SolidLine):
        super().__init__(parent)
        self.dialog_ui = Ui_ThicknessDialog()
        self.dialog_ui.setupUi(self)

        self.__thickness = thickness
        self.__penStyle = penStyle

        self.setWindowTitle(str)

        self.__initData()

    #  ==============自定义功能函数========================

    def __initData(self):
        self.dialog_ui.rt_thickness = Painter(self, self.__thickness, self.__penStyle)
        self.__slider = self.dialog_ui.thicknessSlider
        self.__colorComboBox = self.dialog_ui.penStyleComboBox
        self.__slider.setValue(self.getThickness())
        self.__slider.valueChanged.connect(self.do_valueChanged)
        self.dialog_ui.thicknessNumber.display(str(self.getThickness()))

    def getThickness(self):
        return self.__thickness

    def getPenStyle(self):
        return self.__penStyle

    # ==============event处理函数==========================

    #  ==========由connectSlotsByName()自动连接的槽函数============

    @Slot(int)
    def on_penStyleComboBox_currentIndexChanged(self, value):
        if value == 0:
            self.__penStyle = Qt.SolidLine
        elif value == 1:
            self.__penStyle = Qt.DashLine
        elif value == 2:
            self.__penStyle = Qt.DotLine
        elif value == 3:
            self.__penStyle = Qt.DashDotLine
        elif value == 4:
            self.__penStyle = Qt.DashDotDotLine

        self.dialog_ui.rt_thickness.setPenStyle(self.__penStyle)

    #  =============自定义槽函数===============================

    def do_valueChanged(self, value):
        self.__thickness = value
        self.dialog_ui.rt_thickness.setThickness(value)
        self.dialog_ui.thicknessNumber.display(str(value))


class Painter(QWidget):

    def __init__(self, parent=None, thickness=3, penStyle=Qt.SolidLine):
        super().__init__(parent)
        self.thickness = thickness
        self.penStyle = penStyle
        self.setFixedWidth(334)
        self.setFixedHeight(50)
        self.width = self.width()
        self.height = self.height()
        self.pen = QPen(QColor(Qt.black), self.thickness, self.penStyle)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        painter.setPen(QPen(QColor(Qt.black), self.thickness, self.penStyle))
        painter.drawLine(20, self.height / 2, self.width, self.height / 2)
        painter.end()
        self.update()

    def setThickness(self, thickness):
        self.thickness = thickness

    def setPenStyle(self, penStyle):
        self.penStyle = penStyle


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = ThicknessDialog()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
