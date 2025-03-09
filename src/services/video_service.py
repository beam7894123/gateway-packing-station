import cv2
import os
from datetime import datetime
from services.config_manager import ConfigManager

class VideoCaptureService: # TODO: Validate this class
    def __init__(self, filename="output.mp4", fps=20, resolution=(640, 480)):
        self.config_manager = ConfigManager()
        self.filename = filename
        self.fps = fps
        self.resolution = resolution
        self.cap = cv2.VideoCapture(0)  # Open webcam
        
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
        self.out = cv2.VideoWriter(self.filename, fourcc, self.fps, self.resolution)

        self.is_recording = False
        self.output_folder = self.config_manager.get_video_location()
        os.makedirs(self.output_folder, exist_ok=True)
        
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
        self.is_recording = True
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(self.output_folder, f"recording_OrderX_{timestamp}.avi")  # TODO: Change to order ID
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 30.0
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.out = cv2.VideoWriter(self.filename, fourcc, fps, (width, height))
        return True
    
    def stop_recording(self):
        self.is_recording = False
        # self.cap.release()
        self.out.release()
        print(f"Video saved as {self.filename}")
        
        # Reopen the camera to keep it available
        # self.cap.release()
        # self.cap = cv2.VideoCapture(self.config_manager.get_camera_index())

    def write_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, self.resolution)  # Ensure correct resolution
                if self.is_recording:
                    self.out.write(frame)  # Write frame to file
                return frame
            else:
                print("Error: Could not read frame")
        else:
            print("Error: Webcam is not opened")
        return None
        
    def inti_video(self):
        self.cap.release()
        self.cap = cv2.VideoCapture(self.config_manager.get_camera_index())

    def change_camera(self, index):
        self.cap.release()
        self.cap = cv2.VideoCapture(index)
        # self.config_manager.set_camera_index(index) # Save camera index
        if not self.cap.isOpened():
            print(f"Error: Could not open webcam with index {index}")

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