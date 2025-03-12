import asyncio
import json
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QHttpMultiPart, QHttpPart
from PySide6.QtCore import QUrl, QByteArray, QFile, QIODevice, QFileInfo
from services.config_manager import ConfigManager

class APIService:
    def __init__(self):
        self.network_manager = QNetworkAccessManager()

    def get_api_url(self):
        config_manager = ConfigManager()
        return config_manager.get_api_url()

    async def get_data(self, endpoint):
        url = QUrl(f"{self.get_api_url()}{endpoint}")
        request = QNetworkRequest(url)
        future = asyncio.Future()  # Create Future for async handling

        reply = self.network_manager.get(request)

        # Handle response
        def handle_reply():
            response_data = None
            try:
                # Always try to read the response, even if there's an error
                raw_data = reply.readAll().data().decode('utf-8')
                response_data = json.loads(raw_data) if raw_data else None
            except json.JSONDecodeError:
                response_data = {"error": "Invalid JSON response"}

            if reply.error() == QNetworkReply.NoError:
                print(f"✅ Response: {response_data}")  # Debugging
            else:
                print(f"❌ Error ({reply.error()}): {reply.errorString()}")
                print(f"🔹 Server Response: {response_data}")  # Log the JSON response

            future.set_result(response_data)  # Return JSON data (even on error)
            reply.deleteLater()

        reply.finished.connect(handle_reply)
        return await future


    async def post_data(self, endpoint, data, callback=None, file_path=None):
        url = QUrl(f"{self.get_api_url()}{endpoint}")
        request = QNetworkRequest(url)
        future = asyncio.Future()

        if file_path:
            # Multipart form-data for file upload
            multi_part = QHttpMultiPart(QHttpMultiPart.FormDataType)

            # Add JSON fields
            for key, value in data.items():
                text_part = QHttpPart()
                text_part.setHeader(QNetworkRequest.ContentDispositionHeader, f'form-data; name="{key}"')
                text_part.setBody(str(value).encode('utf-8'))
                multi_part.append(text_part)
            
            file_info = QFileInfo(file_path)
            filename = file_info.fileName()
            file_part = QHttpPart()
            file_part.setHeader(QNetworkRequest.ContentDispositionHeader, f'form-data; name="video"; filename={filename}')
            file_part.setHeader(QNetworkRequest.ContentTypeHeader, "video/mp4")

            file = QFile(file_path)
            if not file.open(QIODevice.ReadOnly):
                print("Error: Cannot open video file")
                future.set_result(None)
                return await future

            file_part.setBodyDevice(file)
            multi_part.append(file_part)
            file.setParent(multi_part)

            reply = self.network_manager.post(request, multi_part)

        else:
            # Standard JSON POST request
            request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
            json_data = QByteArray(json.dumps(data).encode('utf-8'))
            reply = self.network_manager.post(request, json_data)

        def handle_reply():
            response_data = None
            try:
                # Always try to read the response, even if there's an error
                raw_data = reply.readAll().data().decode('utf-8')
                response_data = json.loads(raw_data) if raw_data else None
            except json.JSONDecodeError:
                response_data = {"error": "Invalid JSON response"}

            if reply.error() == QNetworkReply.NoError:
                print(f"✅ Response: {response_data}")  # Debugging
            else:
                print(f"❌ Error ({reply.error()}): {reply.errorString()}")
                print(f"🔹 Server Response: {response_data}")  # Log the JSON response

            future.set_result(response_data)  # Return JSON data (even on error)
            reply.deleteLater()

            reply.deleteLater()

        reply.finished.connect(handle_reply)
        return await future 
