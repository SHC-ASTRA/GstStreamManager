from PyQt5.QtWidgets import *

from CameraWidget import CameraWidget
import requests

class CameraListWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def populate(self, servers):
        server_urls = ["http://"+server+":5000" for server in servers.split(",")]

        ports_assigned = 0

        for i in range(len(server_urls)):
            url = server_urls[i]
            response = requests.get(url+"/cameras")
            data = response.json()

            server_name = requests.get(url+"/name").text

            count = 0
            for device in data:
                encodings = data[device]["encodings"]
                if len(encodings) == 0:
                    continue
                
                cam_widget = CameraWidget(server_name, url, 11429+ports_assigned, device, encodings)
                self.layout.addWidget(cam_widget, count, i)
                ports_assigned += 1
                count += 1
            