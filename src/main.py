import sys
from PySide6.QtWidgets import QApplication
from views.main_ui import MainStationWindow
import PySide6.QtAsyncio as QtAsyncio

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainStationWindow()
    main_window.show()

    QtAsyncio.run(handle_sigint=True)