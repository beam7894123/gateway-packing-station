from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class AboutPopup(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("About :3")
        self.setFixedSize(300, 200)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create QLabel for text
        about_text = QLabel('Packing station application.\nVersion A1.0\n\nAuthor: BezaTheCat\n')
        about_text.setAlignment(Qt.AlignCenter)

        cat_text = QLabel('Meoww!')
        cat_text.setAlignment(Qt.AlignCenter)
        cat = QLabel('        へ         ╱|、\n   ૮  -   ՛ ) つ(>   < 7  \n    /   ⁻  ៸           、˜〵     \n 乀 (ˍ,   ل            じしˍ,)ノ ')
        cat.setAlignment(Qt.AlignCenter)
        
        # Create Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        
        # Add widgets to layout
        layout.addWidget(about_text)
        layout.addWidget(cat_text)
        layout.addWidget(cat)
        layout.addWidget(close_button)
        
        # Set layout to the QWidget
        self.setLayout(layout)
