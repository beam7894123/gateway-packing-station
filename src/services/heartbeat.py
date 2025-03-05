from PySide6.QtCore import QRunnable, Signal, QObject
from services.api_service import APIService

class StatusCheckWorker(QObject):
    status_signal = Signal(bool)

    def __init__(self):
        super().__init__()

    def check_status(self):
        is_online = False
        try:
            response = APIService.get_data('/packing-station/heartbeat')

            is_online = response.get('status', 'Error') == 'OK'
        except Exception as e:
            is_online = False
            # print(f"Error: {e}")
        
        self.status_signal.emit(is_online)  # Emit the result to the main thread

class StatusCheckRunnable(QRunnable):
    def __init__(self, worker):
        super().__init__()
        self.worker = worker

    def run(self):
        self.worker.check_status()  # Run the status check in the background