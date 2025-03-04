from PySide6.QtCore import QSettings

class ConfigManager:
    def __init__(self):
        self.settings = QSettings("Offical(Real)MaowMeowC0rporati0nXD", "PackingStationGateway")

    def set_api_url(self, url):
        self.settings.setValue("api_url", url)

    def get_api_url(self):
        return self.settings.value("api_url", "http://localhost:3000")  # Default
    
    # TODO Add first time setup method here
    