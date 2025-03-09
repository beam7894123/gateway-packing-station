import os
import cv2
from datetime import datetime
from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
from views.ui.cameraUi import Ui_cameraWidget
from services.video_service import VideoCaptureService
from services.config_manager import ConfigManager

class SettingsCameraWindow(QDialog, Ui_cameraWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Camera Settings")
        self.config_manager = ConfigManager()
        self.video_service = VideoCaptureService()
        self.recording = False
        
        # Camera selection
        self.cameraSelect.addItems(self.video_service.get_available_cameras())
        self.cameraSelect.currentIndexChanged.connect(self.change_camera)
        self.cameraSelect.setCurrentIndex(self.video_service.config_manager.get_camera_index())
        
        # Camera view
        self.video_service.inti_video()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.update_frame()
        
        # Location settings
        self.locationSelect.setText(self.config_manager.get_video_location())
        self.locationSelect.textChanged.connect(self.validate_location) 
        self.locationBrowserButton.clicked.connect(self.browse_location)
        
        # Elements settings
        self.timeStampCheckBox.setChecked(True)
        self.timeStampCheckBox.setDisabled(True)
        self.orderIdCheckBox.setChecked(True)
        self.orderIdCheckBox.setDisabled(True)

        
        # Buttons
        self.record_button.clicked.connect(self.toggle_recording)
        self.saveButton.clicked.connect(self.onSaveButtonPressed)
        self.cancelButton.clicked.connect(self.onCancelButtonPressed)
        
        
    # Video settings ========================================
    def update_frame(self):
        frame = self.video_service.write_frame()
        if frame is not None:
            frame = self.video_service.add_timestamp(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            qimg = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(qimg))
            
        if self.recording and frame is not None:
            self.video_service.out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
    def change_camera(self, index):
        self.video_service.change_camera(index)
        
    def toggle_recording(self):
        if self.video_service.toggle_recording():
            self.recording = True
            self.record_button.setText("Stop Recording")
        else:
            self.recording = False
            self.record_button.setText("Start Recording")
        
           
        
    # Location settings ========================================
    def browse_location(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if folder:
            self.locationSelect.setText(folder)
            self.validate_location()
    
    def validate_location(self):
        folder = self.locationSelect.text().strip()
        if os.path.isdir(folder):
            self.locationSelect.setStyleSheet("border: 1px solid green;")
        else:
            self.locationSelect.setStyleSheet("border: 1px solid red;")

    
    #Other functions ========================================
    def onSaveButtonPressed(self):
        self.config_manager.set_camera_index(self.cameraSelect.currentIndex())
        self.config_manager.set_video_location(self.locationSelect.text())
        self.close()
        
    def onCancelButtonPressed(self):
        self.close()

    def closeEvent(self, event):
        self.video_service.cap.release()
        if self.video_service.out:
            self.video_service.out.release()
        event.accept()