import cv2
import os
import resource_rc # Don't remove this line!
from datetime import datetime
from services.config_manager import ConfigManager
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class VideoCaptureService:
    def __init__(self, filename="output.mp4", fps=30, preview_width=320):
        self.config_manager = ConfigManager()
        self.filename = filename
        self.fps = fps
        self.preview_width = preview_width
        self.preview_height = int((self.preview_width * 3) / 4)
        self.preview_resolution = (self.preview_width, self.preview_height)
        self.cap = cv2.VideoCapture(0)  # Open webcam 0 by default
        
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            self.is_video_available = False
        else:
            self.is_video_available = True
        
        # Get the webcam's native resolution
        self.resolution = (
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  # Width
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Height
        )
            
        self.out = None
        self.is_recording = False
        self.output_folder = self.config_manager.get_video_location()
        os.makedirs(self.output_folder, exist_ok=True)
        
        self.still_image = QPixmap(":no-video.jpg").scaled(
            self.preview_resolution[0], self.preview_resolution[1], Qt.KeepAspectRatio
        )
        
    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
            return False
        else:
            return self.start_recording()

    def start_recording(self):
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            return False
        
        # Get the webcam's actual resolution and frame rate
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        # If the webcam doesn't provide FPS, use a default value (e.g., 30)
        if fps <= 0:
            fps = 30.0
        
        # Set the filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(self.output_folder, f"recording_OrderX_{timestamp}.mp4")
        
        # Initialize VideoWriter with the correct settings
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.filename, fourcc, fps, (width, height))
        
        self.is_recording = True
        return True
    
    def stop_recording(self):
        self.is_recording = False
        if self.out is not None:
            self.out.release()
            self.out = None
            
        print(f"Video saved as {self.filename}")

    def write_frame(self, order_id=None):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, self.resolution) 
                frame = self.add_timestamp(frame)  # Add timestamp
                frame = self.add_order_id(frame, order_id)  # Add order ID
                if self.is_recording and self.out is not None:
                    self.out.write(frame)
                frame_resized = cv2.resize(frame, self.preview_resolution)
                return frame_resized
            else:
                print("Error: Could not read frame")
        else:
            print("Error: Webcam is not opened")
        return None
        
    def inti_video(self):
        if self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(self.config_manager.get_camera_index())
        self.is_video_available = self.cap.isOpened()

    def change_camera(self, index):
        if self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(index)
        self.is_video_available = self.cap.isOpened()

    def set_save_location(self, folder):
        if folder:
            self.output_folder = folder
            
    def get_available_cameras(self, max_tested=5):
        available_cameras = []
        
        for i in range(max_tested):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use DirectShow backend for Windows (optional)
            if cap.isOpened():
                available_cameras.append(f"Camera {i}")
            cap.release()  # Ensure proper release

        return available_cameras

    def add_timestamp(self, frame):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return frame
    
    def add_order_id(self, frame, order_id=None):
        order_text = f"Order {order_id}" if order_id else "[No Order]"
        text_size = cv2.getTextSize(order_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = frame.shape[1] - text_size[0] - 10  # 10 pixels from the right edge
        text_y = frame.shape[0] - 10  # 10 pixels from the bottom edge
        cv2.putText(frame, order_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return frame
    
    def get_still_image(self):
        return self.still_image