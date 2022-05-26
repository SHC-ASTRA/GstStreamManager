from PyQt5.QtWidgets import *

import requests
import signal
from subprocess import Popen

class CameraWidget(QWidget):
    def __init__(self, server, server_url, recv_port, path, encodings):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        camera_list = QComboBox()

        server_label = QLabel(server)
        camera_path_label = QLabel(path)

        self.server_url = server_url
        self.recv_port = recv_port
        self.path = path
        self.encodings = encodings

        self.process = None

        self.encoding_list = QComboBox()
        self.encoding_list.setPlaceholderText("Encoding")
        self.encoding_list.currentTextChanged.connect(self.populate_encoding_arguments)
        self.resolution_list = QComboBox()
        self.resolution_list.setPlaceholderText("Resolution")
        self.framerate_list = QComboBox()
        self.framerate_list.setPlaceholderText("Framerate")

        # Parse Encodings Dictionary
        for encoding in self.encodings.keys():
            self.encoding_list.addItem(encoding)

        start_button = QPushButton("Start") 
        start_button.clicked.connect(self.start_camera_stream)
        pause_button = QPushButton("Pause")
        pause_button.clicked.connect(self.pause_camera_stream)
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_camera_stream)

        layout.addWidget(server_label, 0, 0)
        layout.addWidget(camera_path_label, 0, 1)
        layout.addWidget(self.encoding_list, 1, 0)
        layout.addWidget(self.resolution_list, 1, 1)
        layout.addWidget(self.framerate_list, 1, 2)
        layout.addWidget(start_button, 2, 0)
        layout.addWidget(pause_button, 2, 1)
        layout.addWidget(stop_button, 2, 2)

    def populate_encoding_arguments(self, encoding):
        data = self.encodings[encoding]
        self.resolution_list.clear()
        self.framerate_list.clear()
        self.resolution_list.addItems([str(res) for res in data["resolutions"]])
        self.framerate_list.addItems([str(rate) for rate in data["framerates"]])

    def start_camera_stream(self):
        encoding = self.encoding_list.currentText()
        
        if encoding not in self.encodings or self.resolution_list.currentIndex() < 0 or self.encoding_list.currentIndex() < 0:
            return

        if encoding in ["mjpeg","raw_mjpeg"] and self.process is None:
            self.process = Popen(f"gst-launch-1.0 udpsrc port={self.recv_port} ! application/x-rtp,encoding=JPEG,payload=26 ! rtpjpegdepay ! decodebin ! autovideosink", shell=True)
        elif encoding in ["raw_h264", "h264", "h264_from_mjpeg"] and self.process is None:
            self.process = Popen(f"gst-launch-1.0 udpsrc port={self.recv_port} ! application/x-rtp,encoding=H264 ! rtph264depay ! decodebin ! autovideosink", shell=True)

        res = self.resolution_list.currentIndex()
        width, height = self.encodings[encoding]["resolutions"][res]
        rate = self.framerate_list.currentText()

        params = {
            "path": self.path,
            "encoding": encoding,
            "width": width,
            "height": height,
            "framerate": rate,
            "port": self.recv_port
        }

        requests.get(self.server_url+"/cameras/start", params)

        self.encoding_list.setDisabled(True)
    
    def pause_camera_stream(self):
        params = {
            "path": self.path
        }
        requests.get(self.server_url+"/cameras/stop", params)

    def stop_camera_stream(self):
        self.pause_camera_stream()

        self.encoding_list.setDisabled(False)

        if self.process is None:
            return
        self.process.send_signal(signal.SIGINT)
        self.process.wait()
        self.process = None
