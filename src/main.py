import sys
import assets.resource_rc
import PySide6.QtAsyncio as QtAsyncio
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from views.main_ui import MainStationWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":icon.ico"))
    main_window = MainStationWindow()
    main_window.show()

    QtAsyncio.run(handle_sigint=True)