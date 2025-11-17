import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import os
import socket
import tqdm

SERVER_HOST = "10.245.248.189"  # Change to your MacBook's IP address
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

class FileDragDropWidget(QWidget):
    fileDropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.button = QPushButton("Click to select a file", self)
        self.button.clicked.connect(self.selectFile)
        self.label = QLabel("Drag and Drop a file here", self)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle('File Sender')
        self.setGeometry(400, 400, 300, 200)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        files = [u.toLocalFile() for u in e.mimeData().urls()]
        for f in files:
            self.fileDropped.emit(f)

    def selectFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', os.getenv('HOME'))
        if fname:
            self.fileDropped.emit(fname)

class FileSender(QObject):
    def __init__(self):
        super().__init__()

    def sendFile(self, filepath):
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        s = socket.socket()
        print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
        s.connect((SERVER_HOST, SERVER_PORT))
        print("[+] Connected.")
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filepath, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
        s.close()
        print("[+] File sent.")

def main():
    app = QApplication(sys.argv)
    fileSender = FileSender()
    widget = FileDragDropWidget()
    widget.fileDropped.connect(fileSender.sendFile)
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
