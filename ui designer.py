import cv2
import sys
import datetime
import time
from PySide2.QtCore import QTimer, QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication,QHBoxLayout,QGridLayout,QInputDialog,QLineEdit

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
 
        self.quit_button = QPushButton("退出")
        self.quit_button.clicked.connect(self.close)

        self.recongnize_botton= QPushButton('识别')
        self.recongnize_botton.clicked.connect(self.getText)

        self.save_button=QPushButton('保存图片')
        self.save_button.clicked.connect(self.save_pic)
        
        self.main_layout = QVBoxLayout()  #设定整体窗口垂直布局
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.save_button)
        self.main_layout.addWidget(self.quit_button)
        self.main_layout.addWidget(self.recongnize_botton)
        
 
        self.setLayout(self.main_layout)
 
    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH , self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
 
        self.timer = QTimer()#定时器30毫秒采集一次
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)
 
    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, frame1 = self.capture.read()
        frame = cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1) #水平翻转
        image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))
        global i
        if i==1:
            print('bye')
            cv2.imwrite('F:/python/picture/'+str(time.time())+'.jpg',frame1)
            i=0
    def save_pic(self):
        global i
        print('hello')
        i=1
        #cv2.imwrite('F:/python/picture/'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'.jpg',frame)
    def getText(self):
        text, okPressed = QInputDialog.getText(self, "人脸输入","你的名字（请输入英文）:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)


 
if __name__ == "__main__":
    i=0
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())
