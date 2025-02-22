# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_cameraWidget(object):
    def setupUi(self, cameraWidget):
        if not cameraWidget.objectName():
            cameraWidget.setObjectName(u"cameraWidget")
        cameraWidget.resize(684, 584)
        self.horizontalLayout_2 = QHBoxLayout(cameraWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.camera_label = QLabel(cameraWidget)
        self.camera_label.setObjectName(u"camera_label")

        self.verticalLayout.addWidget(self.camera_label)

        self.camera_select = QComboBox(cameraWidget)
        self.camera_select.setObjectName(u"camera_select")

        self.verticalLayout.addWidget(self.camera_select)

        self.record_button = QPushButton(cameraWidget)
        self.record_button.setObjectName(u"record_button")

        self.verticalLayout.addWidget(self.record_button)

        self.save_button = QPushButton(cameraWidget)
        self.save_button.setObjectName(u"save_button")

        self.verticalLayout.addWidget(self.save_button)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(0, 1)

        self.retranslateUi(cameraWidget)

        QMetaObject.connectSlotsByName(cameraWidget)
    # setupUi

    def retranslateUi(self, cameraWidget):
        cameraWidget.setWindowTitle(QCoreApplication.translate("cameraWidget", u"Form", None))
        self.camera_label.setText(QCoreApplication.translate("cameraWidget", u"camera_label", None))
        self.record_button.setText(QCoreApplication.translate("cameraWidget", u"Start Recording", None))
        self.save_button.setText(QCoreApplication.translate("cameraWidget", u"Set Save Location...", None))
    # retranslateUi

