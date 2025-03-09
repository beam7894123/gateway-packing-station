import cv2
# import asset.resource
from PySide6.QtWidgets import QMainWindow, QMessageBox, QLabel, QDialog, QApplication
from PySide6.QtCore import QEvent, QTimer, QThreadPool
from PySide6.QtGui import QImage, QPixmap
from components.order_list import OrderItem, setup_order_list
from services.barcode_handler import handle_barcode
from services.config_manager import ConfigManager
from services.heartbeat import StatusCheckRunnable, StatusCheckWorker
from services.video_service import VideoCaptureService
from views.settings_api_window import SettingsApiWindow
from views.settings_station_window import SettingsStationWindow
from views.settings_camera_window import SettingsCameraWindow
from views.ui.mainUi import Ui_MainWindow
from views.about import AboutPopup
from views.settings_camera_window import SettingsCameraWindow
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
        
        # status status label
        self.status_label = QLabel("NOT Connected")
        self.status_label.setStyleSheet("background-color: red; color: white; padding: 5px;")
        self.statusBar.addPermanentWidget(self.status_label)
        self.last_online_status = False
        # Setup the worker for status checking
        self.status_worker = StatusCheckWorker()
        self.status_worker.status_signal.connect(self.updateStatusAtStatusBar)
        self.startStatusCheck()
        
        # Video Capture
        self.video_service = VideoCaptureService()
        self.still_image = self.video_service.get_still_image()
        self.start_preview()
        
        # Test buttons
        self.pushButton_test1.clicked.connect(self.onPushButtonTest1Clicked)
        self.pushButton_test2.clicked.connect(self.onPushButtonTest2Clicked)
        
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
    
    # Barcode Handler ========================================================================
    def onTextBarcodeInsertChanged(self):
        self.textBarcodeInsert.setFocus()

    def onTextBarcodeInsertEnterPressed(self):
        barcode_text = self.textBarcodeInsert.text()
        print(f"Barcode: {barcode_text}") # Debug <---------------- NEED REMOVE
        
        handle_barcode(barcode_text, self.config_manager, self.listItemScaned, self.listItemNotScaned, self.statusBar)
            
        self.textBarcodeInsert.clear()
        self.textBarcodeInsert.setFocus()
    
    # Recorder ========================================================================
    def update_frame(self):
        if self.video_service.is_video_available:
            frame = self.video_service.write_frame(order_id=self.config_manager.get_order_id())
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                qimg = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg)
                self.videoCaptureView.setPixmap(pixmap)
        else:
            # Show still image if no video feed is available
            self.videoCaptureView.setPixmap(self.still_image)

    def stop_preview(self):
        self.timer.stop()
        
    def start_preview(self):
        self.video_service.inti_video()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
    
    # Event Handler (Other) ========================================================================
    
    def showCamera(self):
        self.stop_preview()
        settings_cam = SettingsCameraWindow(self.video_service)  # Pass existing service
        settings_cam.exec()
        self.video_service.inti_video()  # Reinitialize with potential new settings
        self.start_preview()

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
            # self.video_service.stop_recording() # Stop recording before closing
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
        if self.video_service.start_recording():
            self.statusBar.showMessage("Recording started...")
        # try:
        #     respon = APIService.get_data('/packing-station/check/items/3')
        #     # print(respon)  # Debug <---------------- NEED REMOVE
            
        #     scanned_items = [
        #         OrderItem(item['image'],
        #                 item['name'],
        #                 item['price'],
        #                 item['scannedQuantity'])  
        #         for item in respon['scanned']
        #     ]
            
        #     unscanned_items = [
        #         OrderItem(item['image'],
        #                 item['name'],
        #                 item['price'],
        #                 item['unscannedQuantity'])  
        #         for item in respon['unscanned']
        #     ]
            
        #     setup_order_list(scanned_items, self.listItemScaned)
        #     setup_order_list(unscanned_items, self.listItemNotScaned)
        #     QApplication.beep()
            
        # except Exception as e:
        #     print(f"Error fetching order data: {e}")
        
    def onPushButtonTest2Clicked(self):
        self.video_service.stop_recording()
        self.statusBar.showMessage("Recording stopped and saved.")
        # order_items = []
        # setup_order_list(order_items, self.listItemScaned)
        # setup_order_list(order_items, self.listItemNotScaned)
        