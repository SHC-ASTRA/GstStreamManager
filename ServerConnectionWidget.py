from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ServerConnectionWidget(QWidget):
    connect = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        self.server_box = QLineEdit("192.168.1.2")
        self.server_box.setPlaceholderText("Server Addresses")
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.__connect)

        layout.addWidget(self.server_box, 0, 0)
        layout.addWidget(connect_button, 0, 1)

    def __connect(self):
        self.connect.emit(self.server_box.text())