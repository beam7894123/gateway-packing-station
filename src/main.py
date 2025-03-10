import sys
import qasync
from PySide6.QtWidgets import QApplication
from views.main_ui import MainStationWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    
    try:
        with loop:
            window = MainStationWindow()
            window.show()
            loop.run_forever()
    finally:
        # Proper cleanup
        if window.video_service.cap.isOpened():
            window.video_service.cap.release()
        app.quit()