# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ThicknessDialog.ui'
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

import res_rc

class Ui_ThicknessDialog(object):
    def setupUi(self, ThicknessDialog):
        if not ThicknessDialog.objectName():
            ThicknessDialog.setObjectName(u"ThicknessDialog")
        ThicknessDialog.resize(350, 250)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ThicknessDialog.sizePolicy().hasHeightForWidth())
        ThicknessDialog.setSizePolicy(sizePolicy)
        ThicknessDialog.setMinimumSize(QSize(350, 250))
        ThicknessDialog.setMaximumSize(QSize(350, 250))
        ThicknessDialog.setAutoFillBackground(True)
        self.verticalLayoutWidget = QWidget(ThicknessDialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 360, 251))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(10, 10, 20, 5)
        self.rt_thickness = QWidget(self.verticalLayoutWidget)
        self.rt_thickness.setObjectName(u"rt_thickness")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rt_thickness.sizePolicy().hasHeightForWidth())
        self.rt_thickness.setSizePolicy(sizePolicy1)
        self.rt_thickness.setMinimumSize(QSize(0, 30))
        self.rt_thickness.setMaximumSize(QSize(334, 30))

        self.verticalLayout.addWidget(self.rt_thickness)

        self.penStyleComboBox = QComboBox(self.verticalLayoutWidget)
        icon = QIcon()
        icon.addFile(u":/icons/images/SolidLine.png", QSize(), QIcon.Normal, QIcon.Off)
        self.penStyleComboBox.addItem(icon, "")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/DashLine.png", QSize(), QIcon.Normal, QIcon.Off)
        self.penStyleComboBox.addItem(icon1, "")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/DotLine.png", QSize(), QIcon.Normal, QIcon.Off)
        self.penStyleComboBox.addItem(icon2, "")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/DashDotLine.png", QSize(), QIcon.Normal, QIcon.Off)
        self.penStyleComboBox.addItem(icon3, "")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/DashDotDotLine.png", QSize(), QIcon.Normal, QIcon.Off)
        self.penStyleComboBox.addItem(icon4, "")
        self.penStyleComboBox.setObjectName(u"penStyleComboBox")
        self.penStyleComboBox.setMinimumSize(QSize(330, 36))
        self.penStyleComboBox.setMaximumSize(QSize(330, 36))
        self.penStyleComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.penStyleComboBox.setIconSize(QSize(180, 30))

        self.verticalLayout.addWidget(self.penStyleComboBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, -1, 5, -1)
        self.thicknessSlider = QSlider(self.verticalLayoutWidget)
        self.thicknessSlider.setObjectName(u"thicknessSlider")
        self.thicknessSlider.setMinimum(1)
        self.thicknessSlider.setMaximum(20)
        self.thicknessSlider.setOrientation(Qt.Horizontal)
        self.thicknessSlider.setTickPosition(QSlider.TicksBelow)

        self.horizontalLayout.addWidget(self.thicknessSlider)

        self.thicknessNumber = QLCDNumber(self.verticalLayoutWidget)
        self.thicknessNumber.setObjectName(u"thicknessNumber")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.thicknessNumber.sizePolicy().hasHeightForWidth())
        self.thicknessNumber.setSizePolicy(sizePolicy2)
        self.thicknessNumber.setMaximumSize(QSize(64, 66))
        self.thicknessNumber.setLayoutDirection(Qt.LeftToRight)
        self.thicknessNumber.setAutoFillBackground(True)
        self.thicknessNumber.setProperty("value", 1.000000000000000)

        self.horizontalLayout.addWidget(self.thicknessNumber)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btnOk = QPushButton(self.verticalLayoutWidget)
        self.btnOk.setObjectName(u"btnOk")

        self.horizontalLayout_2.addWidget(self.btnOk)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.btnCancel = QPushButton(self.verticalLayoutWidget)
        self.btnCancel.setObjectName(u"btnCancel")

        self.horizontalLayout_2.addWidget(self.btnCancel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ThicknessDialog)
        self.btnOk.clicked.connect(ThicknessDialog.accept)
        self.btnCancel.clicked.connect(ThicknessDialog.reject)

        QMetaObject.connectSlotsByName(ThicknessDialog)
    # setupUi

    def retranslateUi(self, ThicknessDialog):
        ThicknessDialog.setWindowTitle(QCoreApplication.translate("ThicknessDialog", u"Dialog", None))
        self.penStyleComboBox.setItemText(0, QCoreApplication.translate("ThicknessDialog", u"SolidLine", None))
        self.penStyleComboBox.setItemText(1, QCoreApplication.translate("ThicknessDialog", u"DashLine", None))
        self.penStyleComboBox.setItemText(2, QCoreApplication.translate("ThicknessDialog", u"DotLine", None))
        self.penStyleComboBox.setItemText(3, QCoreApplication.translate("ThicknessDialog", u"DashDotLine", None))
        self.penStyleComboBox.setItemText(4, QCoreApplication.translate("ThicknessDialog", u"DashDotDotLine", None))

        self.btnOk.setText(QCoreApplication.translate("ThicknessDialog", u"OK", None))
        self.btnCancel.setText(QCoreApplication.translate("ThicknessDialog", u"Cancel", None))
    # retranslateUi

