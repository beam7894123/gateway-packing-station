import json
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl, QByteArray
from services.config_manager import ConfigManager

class APIService:
    def __init__(self):
        self.network_manager = QNetworkAccessManager()

    def get_api_url(self):
        config_manager = ConfigManager()
        return config_manager.get_api_url()

    def get_data(self, endpoint, callback):
        url = QUrl(f"{self.get_api_url()}{endpoint}")
        request = QNetworkRequest(url)
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self._handle_response(reply, callback))

    def post_data(self, endpoint, data, callback):
        url = QUrl(f"{self.get_api_url()}{endpoint}")
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        json_data = QByteArray(json.dumps(data).encode('utf-8'))
        reply = self.network_manager.post(request, json_data)
        reply.finished.connect(lambda: self._handle_response(reply, callback))

    def _handle_response(self, reply, callback):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll().data().decode('utf-8')
            callback(json.loads(data))
        else:
            print(f"Error: {reply.errorString()}")
            callback(None)
        reply.deleteLater()