import sys
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PySide6.QtCore import QEvent
from PySide6.QtGui import QPalette, QColor
from views.mainUi import Ui_MainWindow
from components.about import AboutPopup
from components.camera import CameraSettingPopup


class MainStationWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        self.setWindowTitle("Station TEST")
        self.textBarcodeInsert.setFocus()

        self.actionExit.triggered.connect(self.closeEvent)

        self.about_window = None
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionAboutQT.triggered.connect(self.showAboutQt)

        self.pushButton.clicked.connect(self.onButtonClicked)

        
        self.app.installEventFilter(self)
        self.textBarcodeInsert.textChanged.connect(self.onTextBarcodeInsertChanged)
        self.textBarcodeInsert.returnPressed.connect(self.onTextBarcodeInsertEnterPressed)

        self.cameraSetting_window = None
        self.actionCamera.triggered.connect(self.showCamera)


    def onButtonClicked(self):
        self.textBarcodeInsert.setFocus()

    def onTextBarcodeInsertChanged(self):
        self.textBarcodeInsert.setFocus()

    def onTextBarcodeInsertEnterPressed(self):
        barcode_text = self.textBarcodeInsert.text()
        print(f"Barcode: {barcode_text}") # Add Barcode API call here <---------------
        self.textBarcodeInsert.clear()
        self.textBarcodeInsert.setFocus()

    def showCamera(self):
        if self.cameraSetting_window is None or not self.cameraSetting_window.isVisible():
            self.cameraSetting_window = CameraSettingPopup(app)
            self.cameraSetting_window.show() 


    # Bug PLZ FIX! --> when click on the close button, the window will close but will appear again
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()
        else:
            QApplication.quit()
            # event.ignore()

    
    def showAbout(self):
        if self.about_window is None or not self.about_window.isVisible():
            self.about_window = AboutPopup()
            self.about_window.show() 

    def showAboutQt(self):
        QApplication.aboutQt()

    # Ensure focus on textBarcodeInsert is set when the window opens
    def showEvent(self, event):
        super().showEvent(event)
        self.textBarcodeInsert.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if obj != self.textBarcodeInsert:
                self.textBarcodeInsert.setFocus()
        return super().eventFilter(obj, event)

#  Light mode fixed --------------------------------------------------------------------------------------------
def set_light_mode(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(240, 240, 240))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.placeholderText, QColor(0, 0, 0))
    app.setPalette(palette)

# MAIN --------------------------------------------------------------------------------------------
app = QApplication(sys.argv)
w = MainStationWindow(app)
# app.setStyle("Fusion")  # Ensures consistent style across platforms
# set_light_mode(app)  # Apply light mode
w.show()
app.exec()