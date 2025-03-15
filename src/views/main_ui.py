import asyncio
import cv2
import assets.resource_rc
from PySide6.QtWidgets import QMainWindow, QMessageBox, QLabel, QDialog
from PySide6.QtCore import QEvent, QTimer, QDateTime
from PySide6.QtGui import QImage, QPixmap
from components.order_list import OrderItem, setup_order_list
from components.pop_up import Popup
from services.barcode_handler import BarcodeHandler
from services.config_manager import ConfigManager
from services.heartbeat import StatusCheckWorker
from services.video_service import VideoCaptureService
from services.api_service import APIService
from views.settings_api_window import SettingsApiWindow
from views.settings_station_window import SettingsStationWindow
from views.settings_camera_window import SettingsCameraWindow
from views.ui.mainUi import Ui_MainWindow
from views.about import AboutPopup
from views.settings_camera_window import SettingsCameraWindow

class MainStationWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # TODO: Add force for textBarcodeInsert
        super().__init__()
        self.setupUi(self)
        self.config_manager = ConfigManager()
        self.api_service = APIService()
        self.checkFirstTimeSetup()
        self.orderLeftCheck()
        self.setMainWindowTitle()

        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionAboutQT.triggered.connect(self.showAboutQt)
        self.actionCamera.triggered.connect(self.showCamera)
        self.actionApiSetting.triggered.connect(self.showApiSettings)
        self.actionStation.triggered.connect(self.showStationSettings)
        
        # Barcode
        self.textBarcodeInsert.returnPressed.connect(lambda: asyncio.ensure_future(self.onTextBarcodeInsertEnterPressed()))
        self.textBarcodeInsert.installEventFilter(self)
        self.set_status_label(0)
        
        # status status label
        self.status_label = QLabel("NOT Connected")
        self.status_label.setStyleSheet("background-color: red; color: white; padding: 5px;")
        self.statusBar.addPermanentWidget(self.status_label)
        self.last_online_status = False
        self.status_worker = StatusCheckWorker()
        self.status_worker.status_signal.connect(self.updateStatusAtStatusBar)
        self.startStatusCheck()
        
        # Video Capture
        """ WARN!: If any function use VideoCaptureService, it must use video_service as a parameter from main only! """
        """ (This mf wasted my 3 day work to find out why the video keep fram error damn! TwT) """
        self.video_service = VideoCaptureService() 
        self.video_service.init_video()
        self.start_preview()
        
        #Log window
        self.logWindow.setReadOnly(True)
        self.barcode_handler = BarcodeHandler()
        self.barcode_handler.log_signal.connect(self.add_log_entry)
        self.barcode_handler.barcode_scanned.connect(self.handle_barcode_scan)
        
        #Big buttons
        self.bigRightDownButtonConfig()
        
    # StatusCheck ========================================================================
    def startStatusCheck(self):
        self.statusBar.showMessage("Checking API...")
        self.status_label.setText("Reconnecting")
        self.status_label.setStyleSheet("background-color: #8B8000; color: white; padding: 5px;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: asyncio.ensure_future(self.status_worker.check_status()))
        self.timer.start(30000)  # Don't check lower than 10 seconds it will be break XD
        QTimer.singleShot(2000, self.checkStatusInBackground)  # Check the status immediately (2 sec after Just incase)

    def checkStatusInBackground(self):
        asyncio.ensure_future(self.status_worker.check_status())
        
    def updateStatusAtStatusBar(self, is_online):
        if self.last_online_status == is_online:
            return
        
        if is_online:
            self.status_label.setText("Connected!")
            self.status_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
            self.statusBar.showMessage("Connected to API server!", 3000)
            self.add_log_entry("Connected to server!", "success")
            self.set_status_label(0)
        else:
            self.status_label.setText("NOT Connected")
            self.status_label.setStyleSheet("background-color: red; color: white; padding: 5px;")
            self.statusBar.showMessage("Failed to connect to API server", 5000)
            self.add_log_entry(f"Failed to connect to server ({self.config_manager.get_api_url()})", "error")
            self.set_status_label(5)
            
        # Update the last known status
        self.last_online_status = is_online
    
    def onApiSettingsSaved(self, result):
        if result == QDialog.Accepted:
            self.statusBar.showMessage("Checking API...")
            self.status_label.setStyleSheet("background-color: #8B8000; color: white; padding: 5px;")
            if self.last_online_status:
                self.status_label.setText("Reconnecting")
                self.add_log_entry("Reconnecting to server...", "warning")
                self.last_online_status = None
            else:
                self.status_label.setText("Reconnecting")
                self.add_log_entry("Reconnecting to server...", "warning")
                self.last_online_status = None
                
            self.checkStatusInBackground()
    
    # Help Actions ========================================================================
    def showAbout(self):
        about_window = AboutPopup()
        about_window.exec()

    def showAboutQt(self):
        QMessageBox.aboutQt(self)
    
    # Barcode Handler ========================================================================
    async def onTextBarcodeInsertEnterPressed(self):
        barcode_text = self.textBarcodeInsert.text()
        # print(f"Barcode: {barcode_text}")
        
        await self.barcode_handler.handle_barcode(
            barcode_text,
            self.config_manager,
            self.video_service,
            self.listItemScaned,
            self.listItemNotScaned,
            self.statusBar,
            self.set_status_label,
        )
            
        self.textBarcodeInsert.clear()
        
    def eventFilter(self, obj, event):
        if obj == self.textBarcodeInsert:
            if event.type() == QEvent.FocusIn:
                self.textBarcodeInsert.setStyleSheet("font-size: 24px; font-weight: bold;")
                self.textBarcodeInsert.setPlaceholderText("INSERT BARCODE TEXT HERE")
            elif event.type() == QEvent.FocusOut:
                self.textBarcodeInsert.setStyleSheet("background-color: #8B8000; font-size: 24px; font-weight: bold;")
                self.textBarcodeInsert.setPlaceholderText("CLICK HERE TO START THE SCAN")
        return super().eventFilter(obj, event)
        
    # Status Label ========================================================================
    def set_status_label(self, status_code):
        self.is_recording_animation_active = False
        if status_code == 0:  # Standby
            self.bigRightDownButtonConfig()
            self.statusLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background-color: green;")
            self.statusLabel.setText("STATUS: STANDBY")
        elif status_code == 1:  # Recording
            self.statusLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background-color: red;")
            self.is_recording_animation_active = True
            self.start_rec_animation()
            self.toggleRecordingButton()
        elif status_code == 2:  # Processing
            self.bigRightDownButtonConfig()
            self.statusLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background-color: #8B8000;")
            self.statusLabel.setText("STATUS: PROCESSING")
        elif status_code == 3:  # Error
            self.bigRightDownButtonConfig()
            self.statusLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background-color: #000;")
            self.statusLabel.setText("STATUS: ERROR")
        elif status_code == 5:  # Error
            self.bigRightDownButtonConfig()
            self.statusLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background-color: #000;")
            self.statusLabel.setText("ERROR: Check API")
            
    def start_rec_animation(self):
        if not self.is_recording_animation_active:
            return
        self.statusLabel.setText("STATUS: RECORDING")
        QTimer.singleShot(500, lambda: self.statusLabel.setText("STATUS: RECORDING.") if self.is_recording_animation_active else None)
        QTimer.singleShot(1000, lambda: self.statusLabel.setText("STATUS: RECORDING..") if self.is_recording_animation_active else None)
        QTimer.singleShot(1500, lambda: self.statusLabel.setText("STATUS: RECORDING...") if self.is_recording_animation_active else None)
        QTimer.singleShot(2000, self.start_rec_animation)

    # Camera Preview & Recorder ========================================================================
    def update_frame(self):
        try:
            frame = self.video_service.write_frame()
            if frame is None:
                frame = self.video_service.last_valid_frame
                
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                qimg = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
                self.videoCaptureView.setPixmap(QPixmap.fromImage(qimg))
        except Exception as e:
            print(f"UI frame update error: {str(e)}")
            self.videoCaptureView.setPixmap(self.video_service.still_image)

    def stop_preview(self):
        self.timer.stop()
        
    def start_preview(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.update_frame()
        
    def showCamera(self):
        self.stop_preview()
        settings_cam = SettingsCameraWindow(self.video_service)  # Pass existing service
        settings_cam.exec()
        self.video_service.init_video()  # Reinitialize with potential new settings
        self.start_preview()
        self.add_log_entry("Camera reinitialized!", "info")
    
    # Start up ========================================================================
    def checkFirstTimeSetup(self):
        firstTime = self.config_manager.get_first_time_setup()
        if firstTime == True:
            QMessageBox.information(self, "Setup Wizard", "Look like it's your first time setting up in this computer! \nPlease configure the API and Station settings.")
            self.showApiSettings()
            self.showStationSettings()
            self.config_manager.set_first_time_setup(False)
            
    def orderLeftCheck(self):
        if self.config_manager.get_is_order_status_free() == False:
            warn = QMessageBox.warning(self, 'Warning', f'It look like you still have unfulfill Order {self.config_manager.get_order_id()}.\nDo you want to reset this order? ', QMessageBox.Reset | QMessageBox.Reset, QMessageBox.No)
            if warn == QMessageBox.Reset:
                self.config_manager.clear_order_id()
            if warn == QMessageBox.No:
                return
    
    # Event Handler (Other) ========================================================================
    
    def add_log_entry(self, message, message_type="info"):
        timestamp = QDateTime.currentDateTime().toString("[yyyy-MM-dd hh:mm:ss]")
        color = {
            "success": "#4CAF50",
            "error": "#F44336",
            "warning": "#FFC107",
            "info": "#2196F3"
        }.get(message_type, "#FFFFFF")

        html = f"""
        <div style="margin: 2px 0;">
            <span style="color: #757575;">{timestamp}</span>
            <span style="color: {color};">▶</span>
            <span style="color: {color};">{message}</span>
        </div>
        """
        
        # Keep only last 1000 lines
        current_length = self.logWindow.document().blockCount()
        if current_length > 1000:
            self.logWindow.clear()
            
        self.logWindow.append(html)
        self.logWindow.verticalScrollBar().setValue(
            self.logWindow.verticalScrollBar().maximum()
        )
        
    def handle_barcode_scan(self, barcode_data):
        """Handle barcode scan event"""
        self.add_log_entry(f"Processing barcode: {barcode_data}", "info")
        # You can add additional logic here for database checking, etc.

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
        
    def bigRightDownButtonConfig(self):
        self.rightDownButton.setEnabled(False)
        self.rightDownButton.setText("")

    def toggleRecordingButton(self):
        if self.video_service.is_recording:
            self.rightDownButton.setText("Stop Recording")
            
            self.rightDownButton.clicked.connect(lambda: asyncio.ensure_future(self.clear_order()))
            self.rightDownButton.setEnabled(True)
    
    async def clear_order(self):
        reply = QMessageBox.warning(self, 'Warning', 'Are you sure you want to abandon this order?\nYour progress will be lost!', 
                                     QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.video_service.stop_recording()
            self.add_log_entry(f"Stopped recording (Order ID: {self.config_manager.get_order_id()})", "info")
            self.set_status_label(2)
            await asyncio.sleep(1)
            await self.clear_order_api()
            setup_order_list([], self.listItemScaned)
            setup_order_list([], self.listItemNotScaned)
            self.add_log_entry(f"Order ID: {self.config_manager.get_order_id()} abandoned!", "warning")
            self.config_manager.clear_order_id()
            self.set_status_label(0)
            self.bigRightDownButtonConfig()
            self.statusBar.showMessage("Order Cleared!")
            
    async def clear_order_api(self):
        try:
            await self.api_service.post_data(
                    '/packing-station/finish',
                    {
                        'orderId': self.config_manager.get_order_id(),
                        'station': self.config_manager.get_station_id(),
                        'status': 0
                    },
                )
        except Exception as e:
            self.add_log_entry(f"Error sending Order ID: {self.config_manager.get_order_id()} data!", "error")
            print(f"Error sending order data: {str(e)}")
            self.set_status_label(3)
    
    def closeEvent(self, event): # 3 if else statement lol
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.config_manager.get_is_order_status_free() == False:
                lastWarn = QMessageBox.warning(self, 'Warning', f'It look like you still have unfulfill Order {self.config_manager.get_order_id()}.\nAre you REALLY sure you want to quit? ', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if lastWarn == QMessageBox.Yes:
                    self.video_service.stop_recording()
                    event.accept()
                else:
                    event.ignore()
            else:
                event.accept()
        else:
            event.ignore()