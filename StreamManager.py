import sys

from PyQt5.QtWidgets import *

import CameraAddWidget as caw
import CameraListWidget as clw
import CameraWidget as cw
import ServerConnectionWidget as scw

class Screen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gstreamer Manager")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.server_conn = scw.ServerConnectionWidget()

        self.camera_list = clw.CameraListWidget()
        self.server_conn.connect.connect(self.camera_list.populate)

        layout.addWidget(self.server_conn)
        layout.addWidget(self.camera_list)


def run():
    app = QApplication(sys.argv)
    w = Screen()
    w.show()
    app.exec_()

if __name__ == '__main__':
    run()