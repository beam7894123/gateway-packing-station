import os
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
    
    def get_camera_index(self):
        return self.settings.value("camera_index", 0)
    
    def set_camera_index(self, camera_index):
        self.settings.setValue("camera_index", camera_index)
        
    def get_video_location(self):
        return self.settings.value("video_save_location", os.path.join(os.getcwd(), "camera_records"))
        
    def set_video_location(self, location):
        self.settings.setValue("video_save_location", location)
        
    def get_order_id(self):
        return self.settings.value("current_order_id", "")
    
    def clear_order_id(self):
        self.settings.setValue("current_order_id", "")
    
    def get_is_order_status_free(self):
        if self.get_order_id() == "":
            return True
        else:
            return False
    
    def set_order_id(self, order_id):
        self.settings.setValue("current_order_id", order_id)
    
    def get_first_time_setup(self):
        return self.settings.value("first_time", True)
    
    def set_first_time_setup(self, first_time):
        self.settings.setValue("first_time", first_time)
        
    # TODO: Add order_id and order_status methods for saving order data
    