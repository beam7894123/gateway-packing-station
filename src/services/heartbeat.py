from PySide6.QtCore import Signal, QObject
from services.api_service import APIService

class StatusCheckWorker(QObject):
    status_signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.api_service = APIService()

    def check_status(self):
        self.api_service.get_data('/packing-station/heartbeat', self._handle_response)

    def _handle_response(self, response):
        if response and response.get('status') == 'OK':
            self.status_signal.emit(True)
        else:
            self.status_signal.emit(False)