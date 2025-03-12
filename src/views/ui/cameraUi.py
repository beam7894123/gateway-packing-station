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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_cameraWidget(object):
    def setupUi(self, cameraWidget):
        if not cameraWidget.objectName():
            cameraWidget.setObjectName(u"cameraWidget")
        cameraWidget.resize(678, 664)
        self.horizontalLayout_2 = QHBoxLayout(cameraWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.camera_label = QLabel(cameraWidget)
        self.camera_label.setObjectName(u"camera_label")

        self.verticalLayout.addWidget(self.camera_label, 0, Qt.AlignHCenter)

        self.VideoSettingsGroupBox = QGroupBox(cameraWidget)
        self.VideoSettingsGroupBox.setObjectName(u"VideoSettingsGroupBox")
        self.verticalLayout_3 = QVBoxLayout(self.VideoSettingsGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cameraLabel = QLabel(self.VideoSettingsGroupBox)
        self.cameraLabel.setObjectName(u"cameraLabel")

        self.horizontalLayout_3.addWidget(self.cameraLabel)

        self.cameraSelect = QComboBox(self.VideoSettingsGroupBox)
        self.cameraSelect.setObjectName(u"cameraSelect")

        self.horizontalLayout_3.addWidget(self.cameraSelect)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.locationLabel = QLabel(self.VideoSettingsGroupBox)
        self.locationLabel.setObjectName(u"locationLabel")

        self.horizontalLayout.addWidget(self.locationLabel)

        self.locationSelect = QLineEdit(self.VideoSettingsGroupBox)
        self.locationSelect.setObjectName(u"locationSelect")

        self.horizontalLayout.addWidget(self.locationSelect)

        self.locationBrowserButton = QPushButton(self.VideoSettingsGroupBox)
        self.locationBrowserButton.setObjectName(u"locationBrowserButton")

        self.horizontalLayout.addWidget(self.locationBrowserButton)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.ElementsGroupBox = QGroupBox(self.VideoSettingsGroupBox)
        self.ElementsGroupBox.setObjectName(u"ElementsGroupBox")
        self.verticalLayout_2 = QVBoxLayout(self.ElementsGroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.timeStampCheckBox = QCheckBox(self.ElementsGroupBox)
        self.timeStampCheckBox.setObjectName(u"timeStampCheckBox")

        self.verticalLayout_2.addWidget(self.timeStampCheckBox)

        self.orderIdCheckBox = QCheckBox(self.ElementsGroupBox)
        self.orderIdCheckBox.setObjectName(u"orderIdCheckBox")

        self.verticalLayout_2.addWidget(self.orderIdCheckBox)


        self.verticalLayout_3.addWidget(self.ElementsGroupBox)


        self.verticalLayout.addWidget(self.VideoSettingsGroupBox)

        self.record_button = QPushButton(cameraWidget)
        self.record_button.setObjectName(u"record_button")

        self.verticalLayout.addWidget(self.record_button)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.saveButton = QPushButton(cameraWidget)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_4.addWidget(self.saveButton)

        self.cancelButton = QPushButton(cameraWidget)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_4.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

#if QT_CONFIG(shortcut)
        self.locationLabel.setBuddy(self.locationLabel)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(cameraWidget)

        QMetaObject.connectSlotsByName(cameraWidget)
    # setupUi

    def retranslateUi(self, cameraWidget):
        cameraWidget.setWindowTitle(QCoreApplication.translate("cameraWidget", u"Form", None))
        self.camera_label.setText(QCoreApplication.translate("cameraWidget", u"camera_label", None))
        self.VideoSettingsGroupBox.setTitle(QCoreApplication.translate("cameraWidget", u"Video Settings", None))
        self.cameraLabel.setText(QCoreApplication.translate("cameraWidget", u"Camera:", None))
        self.locationLabel.setText(QCoreApplication.translate("cameraWidget", u"Save Location:", None))
        self.locationBrowserButton.setText(QCoreApplication.translate("cameraWidget", u"Browser", None))
        self.ElementsGroupBox.setTitle(QCoreApplication.translate("cameraWidget", u"Enable/Disable Elements", None))
        self.timeStampCheckBox.setText(QCoreApplication.translate("cameraWidget", u"TimeStamp", None))
        self.orderIdCheckBox.setText(QCoreApplication.translate("cameraWidget", u"Order ID", None))
        self.record_button.setText(QCoreApplication.translate("cameraWidget", u"TEST Start Recording", None))
        self.saveButton.setText(QCoreApplication.translate("cameraWidget", u"Save", None))
        self.cancelButton.setText(QCoreApplication.translate("cameraWidget", u"Cancel", None))
    # retranslateUi

