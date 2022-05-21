from PyQt5.QtWidgets import *

class CameraAddWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        camera_list = QComboBox()
        add_button = QPushButton("Add")

        layout.addWidget(camera_list, 0, 0)
        layout.addWidget(add_button, 0, 1)

