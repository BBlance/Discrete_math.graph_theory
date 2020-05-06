# -*- coding: utf-8 -*-

##  GUI应用程序主程序入口

import sys

from PySide2.QtWidgets import QApplication

from Windows import MainWindow

app = QApplication(sys.argv)  # 创建GUI应用程序
##icon = QIcon(":/icons/images/app.ico")
##app.setWindowIcon(icon)

mainform = MainWindow()  # 创建主窗体

mainform.show()  # 显示主窗体

sys.exit(app.exec_())
