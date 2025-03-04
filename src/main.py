import sys
from PySide6.QtWidgets import QApplication
from views.main_ui import MainStationWindow
from utils import set_light_mode

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # set_light_mode(app)  # Apply light mode <--- NEED FIX
    window = MainStationWindow()
    window.show()
    sys.exit(app.exec())
