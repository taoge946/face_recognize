import cv2
import sys
 
from PySide2.QtCore import QTimer, QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication
 
 
class MainApp(QWidget):
 
    def __init__(self):
        QWidget.__init__(self)#直接继承Widget这个无菜单栏窗口的类
        self.setWindowTitle('人脸识别')
        self.video_size = QSize(1080, 720)
        self.setup_ui()
        self.setup_camera()
 
    def setup_ui(self):
        """Initialize widgets.
        """
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)
 
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
 
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.quit_button)
 
        self.setLayout(self.main_layout)
 
    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH , self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
 
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)
 
    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())
