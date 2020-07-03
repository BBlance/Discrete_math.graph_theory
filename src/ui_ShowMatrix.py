# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ShowMatrix.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_ShowMatrix(object):
    def setupUi(self, ShowMatrix):
        if not ShowMatrix.objectName():
            ShowMatrix.setObjectName(u"ShowMatrix")
        ShowMatrix.resize(274, 210)
        self.verticalLayout = QVBoxLayout(ShowMatrix)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout = QVBoxLayout()
        self.layout.setObjectName(u"layout")

        self.verticalLayout.addLayout(self.layout)

        self.dataView = QTableView(ShowMatrix)
        self.dataView.setObjectName(u"dataView")

        self.verticalLayout.addWidget(self.dataView)


        self.retranslateUi(ShowMatrix)

        QMetaObject.connectSlotsByName(ShowMatrix)
    # setupUi

    def retranslateUi(self, ShowMatrix):
        ShowMatrix.setWindowTitle(QCoreApplication.translate("ShowMatrix", u"Form", None))
    # retranslateUi

