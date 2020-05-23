import sys

from PySide2.QtCore import Slot, Qt, QSize
from PySide2.QtGui import QPainter, QPen, QColor, QIcon
from PySide2.QtWidgets import QDialog, QWidget, QApplication, QComboBox

from ui_CreateFileDialog import Ui_CreateFileDialog


class CreateFileDialog(QDialog):

    def __init__(self, parent=None, width=800, height=600):
        super().__init__(parent)
        self.dialog_ui = Ui_CreateFileDialog()
        self.dialog_ui.setupUi(self)

        self.__width = width
        self.__height = height

        self.setWindowTitle("视图尺寸")

    ##  ============自定义功能函数========================
    def __initData(self):
        self.groupSize = self.dialog_ui.fileSizeGroupBox

    ##  ===========event处理函数==========================

    ##  ========由connectSlotsByName()自动连接的槽函数=========

    ##  ==========自定义槽函数===============================
    def radioBtnState(self):
        if self.dialog_ui.radioButton.isChecked():
            self.__width = 2560
            self.__height = 1440
            pass
        elif self.dialog_ui.radioButton_2.isChecked():
            self.__width = 1920
            self.__height = 1080
            pass
        elif self.dialog_ui.radioButton_3.isChecked():
            self.__width = 1600
            self.__height = 900
            pass
        elif self.dialog_ui.radioButton_4.isChecked():
            self.__width = 1280
            self.__height = 960
            pass
        elif self.dialog_ui.radioButton_5.isChecked():
            self.__width = 800
            self.__height = 600
            pass
        elif self.dialog_ui.radioButton_6.isChecked():
            self.dialog_ui.
            pass

    ##  ============窗体测试程序 ============================


if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = CreateFileDialog()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
