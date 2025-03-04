import cv2
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox, QFileDialog, QVBoxLayout
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
from views.ui.cameraUi import Ui_cameraWidget


def get_available_cameras(max_tested=5):
    available_cameras = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(f"Camera {i}")
            cap.release()
    return available_cameras

class CameraSettingPopup(QWidget, Ui_cameraWidget):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        self.setWindowTitle("Camera Settings")
        self.camera_index = 0
        self.recording = False
        self.video_writer = None
        self.output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
        os.makedirs(self.output_folder, exist_ok=True)
        
        self.capture = cv2.VideoCapture(self.camera_index)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.update_frame()
        
        self.camera_select.addItems(get_available_cameras())
        self.camera_select.currentIndexChanged.connect(self.change_camera)

        self.record_button.clicked.connect(self.toggle_recording)
        self.save_button.clicked.connect(self.set_save_location)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:

            # Add timestamp text overlay
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Set display frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            qimg = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(qimg))
            
            if self.recording and self.video_writer:
                self.video_writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
    def change_camera(self, index):
        self.capture.release()
        self.camera_index = index
        self.capture = cv2.VideoCapture(self.camera_index)
    
    def set_save_location(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if folder:
            self.output_folder = folder
    
    def toggle_recording(self):
        if self.recording:
            self.recording = False
            if self.video_writer:
                self.video_writer.release()
            self.video_writer = None
            self.record_button.setText("Start Recording")
        else:
            if not self.output_folder:
                self.output_folder = os.getcwd()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_path = os.path.join(self.output_folder, f"recording_{timestamp}.avi")
            
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fps = 30.0
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.video_writer = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))
            self.recording = True
            self.record_button.setText("Stop Recording...")
    
    def closeEvent(self, event):
        self.capture.release()
        if self.video_writer:
            self.video_writer.release()
        event.accept()


# TEST ONLY PLEASE REMOVE or comment out
if __name__ == "__main__":
    app = QApplication([])
    window = CameraSettingPopup(app)
    window.show()
    app.exec()
