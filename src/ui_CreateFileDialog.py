# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CreateFileDialog.ui'
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


class Ui_CreateFileDialog(object):
    def setupUi(self, CreateFileDialog):
        if not CreateFileDialog.objectName():
            CreateFileDialog.setObjectName(u"CreateFileDialog")
        CreateFileDialog.resize(400, 300)
        self.horizontalLayout_2 = QHBoxLayout(CreateFileDialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.fileSizeGroupBox = QGroupBox(CreateFileDialog)
        self.fileSizeGroupBox.setObjectName(u"fileSizeGroupBox")
        font = QFont()
        font.setPointSize(12)
        self.fileSizeGroupBox.setFont(font)
        self.fileSizeGroupBox.setLayoutDirection(Qt.LeftToRight)
        self.fileSizeGroupBox.setAlignment(Qt.AlignCenter)
        self.fileSizeGroupBox.setFlat(True)
        self.verticalLayout_3 = QVBoxLayout(self.fileSizeGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.radioButton = QRadioButton(self.fileSizeGroupBox)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_3.addWidget(self.radioButton)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)

        self.radioButton_2 = QRadioButton(self.fileSizeGroupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_3.addWidget(self.radioButton_2)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_6)

        self.radioButton_3 = QRadioButton(self.fileSizeGroupBox)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setCheckable(True)
        self.radioButton_3.setChecked(False)
        self.radioButton_3.setAutoRepeat(True)

        self.verticalLayout_3.addWidget(self.radioButton_3)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_7)

        self.radioButton_4 = QRadioButton(self.fileSizeGroupBox)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setInputMethodHints(Qt.ImhLatinOnly)
        self.radioButton_4.setChecked(False)

        self.verticalLayout_3.addWidget(self.radioButton_4)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_8)

        self.radioButton_5 = QRadioButton(self.fileSizeGroupBox)
        self.radioButton_5.setObjectName(u"radioButton_5")
        self.radioButton_5.setChecked(True)

        self.verticalLayout_3.addWidget(self.radioButton_5)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton_6 = QRadioButton(self.fileSizeGroupBox)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.horizontalLayout.addWidget(self.radioButton_6)

        self.widthEdit = QLineEdit(self.fileSizeGroupBox)
        self.widthEdit.setObjectName(u"widthEdit")

        self.horizontalLayout.addWidget(self.widthEdit)

        self.label = QLabel(self.fileSizeGroupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.heightEdit = QLineEdit(self.fileSizeGroupBox)
        self.heightEdit.setObjectName(u"heightEdit")

        self.horizontalLayout.addWidget(self.heightEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(4, 1)
        self.verticalLayout_3.setStretch(6, 1)
        self.verticalLayout_3.setStretch(10, 1)

        self.verticalLayout.addWidget(self.fileSizeGroupBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.btnOK = QPushButton(CreateFileDialog)
        self.btnOK.setObjectName(u"btnOK")
        font1 = QFont()
        font1.setPointSize(14)
        self.btnOK.setFont(font1)

        self.verticalLayout_2.addWidget(self.btnOK)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.btnCancel = QPushButton(CreateFileDialog)
        self.btnCancel.setObjectName(u"btnCancel")
        font2 = QFont()
        font2.setPointSize(15)
        self.btnCancel.setFont(font2)

        self.verticalLayout_2.addWidget(self.btnCancel)

        self.verticalSpacer = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2.setStretch(0, 2)

        self.retranslateUi(CreateFileDialog)
        self.btnOK.clicked.connect(CreateFileDialog.accept)
        self.btnCancel.clicked.connect(CreateFileDialog.reject)

        QMetaObject.connectSlotsByName(CreateFileDialog)
    # setupUi

    def retranslateUi(self, CreateFileDialog):
        CreateFileDialog.setWindowTitle(QCoreApplication.translate("CreateFileDialog", u"Dialog", None))
        self.fileSizeGroupBox.setTitle(QCoreApplication.translate("CreateFileDialog", u"DrawBoard Size", None))
        self.radioButton.setText(QCoreApplication.translate("CreateFileDialog", u"2560\u00d71440", None))
        self.radioButton_2.setText(QCoreApplication.translate("CreateFileDialog", u"1920\u00d71080", None))
        self.radioButton_3.setText(QCoreApplication.translate("CreateFileDialog", u"1600\u00d7900", None))
        self.radioButton_4.setText(QCoreApplication.translate("CreateFileDialog", u"1280\u00d7960", None))
        self.radioButton_5.setText(QCoreApplication.translate("CreateFileDialog", u"800\u00d7600", None))
        self.radioButton_6.setText("")
        self.label.setText(QCoreApplication.translate("CreateFileDialog", u"\u00d7", None))
        self.btnOK.setText(QCoreApplication.translate("CreateFileDialog", u"OK", None))
        self.btnCancel.setText(QCoreApplication.translate("CreateFileDialog", u"Cancel", None))
    # retranslateUi

