from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QEvent
from PySide6.QtGui import QPalette, QColor
from components.order_list import OrderItem, setup_order_list
from views.settings_api_window import SettingsApiWindow
from views.ui.mainUi import Ui_MainWindow
from views.about import AboutPopup
from views.camera import CameraSettingPopup
from services.api_service import APIService

class MainStationWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Station TEST")
        self.textBarcodeInsert.setFocus()

        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionAboutQT.triggered.connect(self.showAboutQt)
        self.actionCamera.triggered.connect(self.showCamera)
        self.actionApiSetting.triggered.connect(self.showApiSettings)

        self.textBarcodeInsert.textChanged.connect(self.onTextBarcodeInsertChanged)
        self.textBarcodeInsert.returnPressed.connect(self.onTextBarcodeInsertEnterPressed)
        
        self.pushButton_test1.clicked.connect(self.onPushButtonTest1Clicked)
        self.pushButton_test2.clicked.connect(self.onPushButtonTest2Clicked)
        
        


    def onTextBarcodeInsertChanged(self):
        self.textBarcodeInsert.setFocus()

    def onTextBarcodeInsertEnterPressed(self):
        barcode_text = self.textBarcodeInsert.text()
        print(f"Barcode: {barcode_text}") # Debug <---------------- NEED REMOVE
        
        # Start load order data and Start Record <--- NEED ADD
        if barcode_text.startswith("start|"):
            _, order_id = barcode_text.split('|', 1)
            if order_id.isdigit():
                try:
                    order_data = APIService.get_data(f'orders/{order_id}')
                    if order_data:
                        order_items = [
                        OrderItem(item['item']['image'],
                                item['item']['name'],
                                item['item']['price'],
                                item['quantity'])  
                        for item in order_data['orderItems']
                        ]
                    else:
                        print("No data found for this order ID")
                except Exception as e:
                    order_items = []
                    print(f"Error fetching order data: {e}")
            else:
                print("Invalid order ID xwx")
                
            setup_order_list(order_items, self.listItemNotScaned)
            
        self.textBarcodeInsert.clear()
        self.textBarcodeInsert.setFocus()

    def showCamera(self):
        if self.cameraSetting_window is None or not self.cameraSetting_window.isVisible():
            self.cameraSetting_window = CameraSettingPopup()
            self.cameraSetting_window.show()

    def showApiSettings(self):
        settings_api = SettingsApiWindow()
        settings_api.exec()

    def showAbout(self):
        about_window = AboutPopup()
        about_window.exec()

    def showAboutQt(self):
        QMessageBox.aboutQt(self)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def showEvent(self, event):
        super().showEvent(event)
        self.textBarcodeInsert.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if obj != self.textBarcodeInsert:
                self.textBarcodeInsert.setFocus()
        return super().eventFilter(obj, event)
    
    def onPushButtonTest1Clicked(self):
        respon = APIService.get_data('orders/2')
        # print(respon) 
        order_items = [
            OrderItem(item['item']['image'],
                      item['item']['name'],
                      item['item']['price'],
                      item['quantity'])  
            for item in respon['orderItems']
        ]
        setup_order_list(order_items, self.listItemNotScaned)
        
    def onPushButtonTest2Clicked(self):
        order_items = []
        setup_order_list(order_items, self.listItemNotScaned)
        