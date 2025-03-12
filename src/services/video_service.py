import time
import cv2
import os
import resource_rc # Don't remove this line!
from datetime import datetime
from services.config_manager import ConfigManager
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class VideoCaptureService:
    # TODO vidoe is too fast for... some reason... =w=
    def __init__(self, filename="output.mp4", fps=30, preview_width=320):
        self.config_manager = ConfigManager()
        self.filename = filename
        self.fps = fps
        self.preview_width = preview_width
        self.preview_height = int((self.preview_width * 3) / 4)
        self.preview_resolution = (self.preview_width, self.preview_height)
        self.last_video_path = None
        self.order_id = None
        
        # Initialize with safe camera opening
        self.cap = self._safe_camera_init()
        self.is_video_available = self.cap.isOpened()
        
        # Fallback to default camera if configured camera fails
        if not self.is_video_available:
            print("Configured camera failed. Falling back to default camera...")
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.is_video_available = self.cap.isOpened()
        
        # Get the webcam's native resolution
        if self.is_video_available:
            self.resolution = (
                int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            )
        else:
            self.resolution = (640, 480)  # Fallback resolution
            
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
        self.order_id = self.config_manager.get_order_id()
        self.filename = os.path.join(self.output_folder, f"recording_Order{self.order_id}_{timestamp}.mp4")
        
        # Initialize VideoWriter with the correct settings
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        self.out = cv2.VideoWriter(self.filename, fourcc, fps, (width, height))
        
        self.is_recording = True
        return True
    
    def stop_recording(self):
        self.is_recording = False
        if self.out is not None:
            self.out.release()
            self.out = None
        
        self.last_video_path = self.filename    
        print(f"Video saved as {self.filename}")
    
    def get_last_recorded_video(self):
        return self.last_video_path

    def write_frame(self):
        max_attempts = 5  # Maximum recovery attempts
        attempt = 0
        
        while attempt < max_attempts:
            if not self.cap.isOpened():
                # print("Camera not available, attempting recovery...")
                self._recover_camera()
                attempt += 1
                continue  # Skip to next iteration

            ret, frame = self.cap.read()
            if not ret:
                print("Frame read failed, initiating recovery...")
                self._recover_camera()
                attempt += 1
                continue  # Skip to next iteration

            try:
                # Process frame
                processed_frame = cv2.resize(frame, self.resolution)
                processed_frame = self.add_timestamp(processed_frame)
                processed_frame = self.add_order_id(processed_frame)
                last_valid_frame = cv2.resize(processed_frame, self.preview_resolution)
                
                if self.is_recording and self.out is not None:
                    self.out.write(processed_frame)
                    
                return last_valid_frame  # Return valid frame
                
            except Exception as e:
                print(f"Frame processing error: {str(e)}")
                attempt += 1
                continue  # Skip to next iteration

        # If max attempts reached, return cached frame
        print(f"Max recovery attempts ({max_attempts}) reached. Using cached frame.")
        return last_valid_frame
        
    def _safe_camera_init(self, retries=3, delay=1):  # Increased retries and delay
        """Robust camera initialization with retries"""
        for i in range(retries):
            cap = cv2.VideoCapture(self.config_manager.get_camera_index(), cv2.CAP_DSHOW)
            if cap.isOpened() and cap.read()[0]:  # Verify frame can be read
                return cap
            cap.release()  # Ensure proper cleanup
            print(f"Camera init failed attempt {i+1}/{retries}")
            time.sleep(delay)
        return cv2.VideoCapture()
        
    def init_video(self):
        if self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(self.config_manager.get_camera_index(), cv2.CAP_DSHOW)
        self.is_video_available = self.cap.isOpened()
        
    def _recover_camera(self):
        """Full camera reinitialization sequence"""
        try:
            if self.cap.isOpened():
                self.cap.release()
            self.cap = self._safe_camera_init()
            self.is_video_available = self.cap.isOpened()
            
            # Reset video writer if recording
            if self.is_recording and self.out is None:
                self.start_recording()
        except Exception as e:
            print(f"Camera recovery error: {str(e)}")

    def change_camera(self, index):
        if self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
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
    
    def add_order_id(self, frame):
        order_id= self.config_manager.get_order_id()
        order_text = f"Order {order_id}" if order_id else "[No Order]"
        text_size = cv2.getTextSize(order_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = frame.shape[1] - text_size[0] - 10  # 10 pixels from the right edge
        text_y = frame.shape[0] - 10  # 10 pixels from the bottom edge
        cv2.putText(frame, order_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return frame
    
    def get_still_image(self):
        return self.still_image