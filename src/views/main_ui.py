from PySide6.QtWidgets import QMainWindow, QMessageBox, QLabel, QDialog
from PySide6.QtCore import QEvent, QTimer, QThreadPool
from components.order_list import OrderItem, setup_order_list
from services.config_manager import ConfigManager
from services.heartbeat import StatusCheckRunnable, StatusCheckWorker
from views.settings_api_window import SettingsApiWindow
from views.settings_station_window import SettingsStationWindow
from views.ui.mainUi import Ui_MainWindow
from views.about import AboutPopup
from views.camera import CameraSettingPopup
from services.api_service import APIService

class MainStationWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config_manager = ConfigManager()
        self.checkFirstTimeSetup()
        self.setMainWindowTitle()
        self.textBarcodeInsert.setFocus()

        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionAboutQT.triggered.connect(self.showAboutQt)
        self.actionCamera.triggered.connect(self.showCamera)
        self.actionApiSetting.triggered.connect(self.showApiSettings)
        self.actionStation.triggered.connect(self.showStationSettings)

        self.textBarcodeInsert.textChanged.connect(self.onTextBarcodeInsertChanged)
        self.textBarcodeInsert.returnPressed.connect(self.onTextBarcodeInsertEnterPressed)
        
        self.pushButton_test1.clicked.connect(self.onPushButtonTest1Clicked)
        self.pushButton_test2.clicked.connect(self.onPushButtonTest2Clicked)
        
        # status status label
        self.status_label = QLabel("NOT Connected")
        self.status_label.setStyleSheet("background-color: red; color: white; padding: 5px;")
        self.statusBar.addPermanentWidget(self.status_label)
        self.last_online_status = False
        # Setup the worker for status checking
        self.status_worker = StatusCheckWorker()
        self.status_worker.status_signal.connect(self.updateStatusAtStatusBar)
        self.startStatusCheck()
        
    # StatusCheck ========================================================================
    def startStatusCheck(self):
        self.statusBar.showMessage("Checking API...")
        self.status_label.setText("Reconnecting")
        self.status_label.setStyleSheet("background-color: #8B8000; color: white; padding: 5px;")
        self.checkStatusInBackground() # Check the status immediately (Just incase)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkStatusInBackground)
        self.timer.start(30000) # Don't check lower than 10 seconds it will be break XD
        
    def checkStatusInBackground(self):
        status_check_worker = StatusCheckRunnable(self.status_worker)
        QThreadPool.globalInstance().start(status_check_worker)  # Run the worker in the background
        
    def updateStatusAtStatusBar(self, is_online):
        # If the status has not changed, do nothing :3
        if self.last_online_status == is_online:
            return
        
        if is_online:
            self.status_label.setText("Connected!")
            self.status_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
            self.statusBar.showMessage("Connected to API server!", 3000)
        else:
            self.status_label.setText("NOT Connected")
            self.status_label.setStyleSheet("background-color: red; color: white; padding: 5px;")
            self.statusBar.showMessage("Failed to connect to API server", 5000)
            
        # Update the last known status
        self.last_online_status = is_online
    
    def onApiSettingsSaved(self, result):
        if result == QDialog.Accepted:
            self.statusBar.showMessage("Checking API...")
            self.status_label.setStyleSheet("background-color: #8B8000; color: white; padding: 5px;")
            if self.last_online_status:
                self.status_label.setText("Reconnecting")
                self.last_online_status = None
            else:
                self.status_label.setText("Reconnecting")
                self.last_online_status = None
                
            self.checkStatusInBackground()
    
    
    # Help Actions ========================================================================
    def showAbout(self):
        about_window = AboutPopup()
        about_window.exec()

    def showAboutQt(self):
        QMessageBox.aboutQt(self)
    
    
    # Event Handler (Other) ========================================================================
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
                    order_data = APIService.get_data(f'/orders/{order_id}')
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
        settings_api.finished.connect(self.onApiSettingsSaved)
        settings_api.exec()
        
    def showStationSettings(self):
        setting_station = SettingsStationWindow()
        setting_station.finished.connect(self.onStationSettingsSaved)
        setting_station.exec()
        
    def onStationSettingsSaved(self, result):
        if result == QDialog.Accepted:
            self.setMainWindowTitle()
    
    def setMainWindowTitle(self):
        self.setWindowTitle(f"Station ID {self.config_manager.get_station_id()} - Packing Station Gateway")

    def checkFirstTimeSetup(self):
        firstTime = self.config_manager.get_first_time_setup()
        if firstTime == True:
            QMessageBox.information(self, "Setup Wizard", "Look like it's your first time setting up in this computer! \nPlease configure the API and Station settings.")
            self.showApiSettings()
            self.showStationSettings()
            self.config_manager.set_first_time_setup(False)
    
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
        respon = APIService.get_data('/orders/2')
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
        