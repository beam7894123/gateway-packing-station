# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QListView, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QToolBar, QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1027, 743)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAboutQT = QAction(MainWindow)
        self.actionAboutQT.setObjectName(u"actionAboutQT")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionStation = QAction(MainWindow)
        self.actionStation.setObjectName(u"actionStation")
        self.actionCamera = QAction(MainWindow)
        self.actionCamera.setObjectName(u"actionCamera")
        self.actionApiSetting = QAction(MainWindow)
        self.actionApiSetting.setObjectName(u"actionApiSetting")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listItem = QVBoxLayout()
        self.listItem.setObjectName(u"listItem")
        self.textBarcodeInsert = QLineEdit(self.centralwidget)
        self.textBarcodeInsert.setObjectName(u"textBarcodeInsert")
        self.textBarcodeInsert.setFocusPolicy(Qt.StrongFocus)
        self.textBarcodeInsert.setStyleSheet(u"font-size: 24px; font-weight: bold;")

        self.listItem.addWidget(self.textBarcodeInsert)

        self.listItemNotScaned = QListView(self.centralwidget)
        self.listItemNotScaned.setObjectName(u"listItemNotScaned")

        self.listItem.addWidget(self.listItemNotScaned)

        self.listItemScaned = QListView(self.centralwidget)
        self.listItemScaned.setObjectName(u"listItemScaned")

        self.listItem.addWidget(self.listItemScaned)


        self.horizontalLayout_2.addLayout(self.listItem)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy)
        self.statusLabel.setAutoFillBackground(False)
        self.statusLabel.setStyleSheet(u"font-size: 24px; font-weight: bold; color: white;background-color: rgb(255, 0, 0);")
        self.statusLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.statusLabel)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.videoCaptureView = QLabel(self.centralwidget)
        self.videoCaptureView.setObjectName(u"videoCaptureView")

        self.verticalLayout.addWidget(self.videoCaptureView, 0, Qt.AlignHCenter)

        self.logWindow = QTextEdit(self.centralwidget)
        self.logWindow.setObjectName(u"logWindow")

        self.verticalLayout.addWidget(self.logWindow)

        self.rightDownButton = QPushButton(self.centralwidget)
        self.rightDownButton.setObjectName(u"rightDownButton")
        self.rightDownButton.setStyleSheet(u"font-size: 24px; font-weight: bold;")

        self.verticalLayout.addWidget(self.rightDownButton)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 4)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1027, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAboutQT)
        self.menuSetting.addAction(self.actionApiSetting)
        self.menuSetting.addAction(self.actionCamera)
        self.menuSetting.addAction(self.actionStation)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionAboutQT.setText(QCoreApplication.translate("MainWindow", u"AboutQT", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionStation.setText(QCoreApplication.translate("MainWindow", u"Station", None))
        self.actionCamera.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.actionApiSetting.setText(QCoreApplication.translate("MainWindow", u"API", None))
        self.textBarcodeInsert.setPlaceholderText(QCoreApplication.translate("MainWindow", u"BARCODE TEXT INSERT HERE", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"STATUS: ERROR", None))
        self.videoCaptureView.setText(QCoreApplication.translate("MainWindow", u"videoCaptureView", None))
        self.rightDownButton.setText(QCoreApplication.translate("MainWindow", u"rightDownButton", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

