# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataDetails.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_DataDetails(object):
    def setupUi(self, DataDetails):
        if not DataDetails.objectName():
            DataDetails.setObjectName(u"DataDetails")
        DataDetails.resize(274, 218)
        self.verticalLayout_2 = QVBoxLayout(DataDetails)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.dataTable = QTableView(DataDetails)
        self.dataTable.setObjectName(u"dataTable")

        self.verticalLayout_2.addWidget(self.dataTable)


        self.retranslateUi(DataDetails)

        QMetaObject.connectSlotsByName(DataDetails)
    # setupUi

    def retranslateUi(self, DataDetails):
        DataDetails.setWindowTitle(QCoreApplication.translate("DataDetails", u"Form", None))
    # retranslateUi

