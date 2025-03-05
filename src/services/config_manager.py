from PySide6.QtCore import QSettings

class ConfigManager:
    def __init__(self):
        self.settings = QSettings("Offical(Real)MaowMeowC0rporati0nXD", "PackingStationGateway")

    def set_api_url(self, url):
        self.settings.setValue("api_url", url)

    def get_api_url(self):
        return self.settings.value("api_url", "http://localhost:3000")  # Default
    
    def set_station_id(self, station_id):
        self.settings.setValue("station_id", station_id)
        
    def get_station_id(self):
        return self.settings.value("station_id", "0")
    
    def get_first_time_setup(self):
        return self.settings.value("first_time", True)
    
    def set_first_time_setup(self, first_time):
        self.settings.setValue("first_time", first_time)
    