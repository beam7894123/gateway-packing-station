from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from services.config_manager import ConfigManager

class SettingsStationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Station ID settings")
        self.config_manager = ConfigManager()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Station ID:")
        self.url_input = QLineEdit(self.config_manager.get_station_id())

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_url)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def save_url(self):
        self.config_manager.set_station_id(self.url_input.text())
        self.accept()  # Closes the dialog