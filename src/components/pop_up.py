from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer

class Popup(QDialog):
    def __init__(self, message="This box will close in 5 seconds!", timeout=1000):
        super().__init__()

        self.setWindowTitle("Notification")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)  # Frameless & click-outside dismissable

        # Set up layout and message label
        layout = QVBoxLayout(self)
        label = QLabel(message, self)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        self.setLayout(layout)
        self.setFixedSize(300, 150)  # Set a fixed size for the popup

        # Auto-close after timeout
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(timeout)

    def mousePressEvent(self, event):
        """Close the dialog if the user clicks outside."""
        self.close()
