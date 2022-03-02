import cv2
import sys
import get_faces_from_camera
import features_extraction_to_csv   
import dlib
import time
import csv
import numpy as np
from PySide2.QtCore import QTimer, QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication,QHBoxLayout,QMessageBox,QInputDialog,QLineEdit,QTextBrowser
import os
import face_reco_from_camera_ot_single_person
from retinaface import Retinaface

path_images_from_camera = "data/data_faces_from_camera/"

class MainApp(QWidget):
 
    def __init__(self):
        QWidget.__init__(self)#直接继承Widget这个无菜单栏窗口的类
        self.setWindowTitle('人脸识别--by李金涛')
        self.video_size = QSize(1080, 720)
        self.floader_flag=0
        self.save_flag=0
        self.rec_flag=0
        self.setup_ui()
        self.setup_camera()
        self.name=''
        self.current_face_dir=''
        
    def setup_ui(self):
        """Initialize widgets.
        """
        self.image_label = QLabel()
        #self.image_label.setFixedSize(self.video_size)
 
        self.quit_button = QPushButton("退出")
        self.quit_button.clicked.connect(self.close)

        self.recognize_botton= QPushButton('识别')
        self.recognize_botton.clicked.connect(self.recognize)

        self.result=QLineEdit()

        self.save_button=QPushButton('保存图片')
        self.save_button.clicked.connect(self.save_pic)

        self.new_floader_button=QPushButton('创建新的人物')
        self.new_floader_button.clicked.connect(self.create_floder)

        self.face_feature_button=QPushButton('提取库中人脸特征')
        self.face_feature_button.clicked.connect(self.feature)

        self.delet_button=QPushButton('删除所有人物数据')
        self.delet_button.clicked.connect(self.delet)
        
        self.main_layout = QVBoxLayout()  #设定整体窗口垂直布局
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.result)
        self.main_layout.addWidget(self.new_floader_button)
        self.main_layout.addWidget(self.save_button)
        self.main_layout.addWidget(self.face_feature_button)
        self.main_layout.addWidget(self.recognize_botton)
        self.main_layout.addWidget(self.delet_button)
        self.main_layout.addWidget(self.quit_button)
        
 
        self.setLayout(self.main_layout)
 
    #def floder_init(self):


    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH , self.video_size.width())
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
 
        self.timer = QTimer()#定时器30毫秒采集一次
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)
 
    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        height=0
        width=0
        Face_Register_con.pre_work_mkdir()
        
        _, frame1 = self.capture.read()
        frame = cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR)                                                                                    
        #frame = cv2.flip(frame, 1) #水平翻转
        frame,b = retinaface.detect_image(frame)
        faces = detector(frame, 0)
        b=np.array(b)
        # if len(faces) != 0:
        #         # 矩形框 / Show the ROI of faces
        #         for k, d in enumerate(faces):
        #             # 计算矩形框大小 / Compute the size of rectangle box
        #             height = (b[3] - b[1])
        #             width = (b[2] - b[0])
        #             hh = int(height/2)
        #             ww = int(width/2)


        #             cv2.rectangle(frame,
        #                           tuple([b[0] - ww, b[1] - hh]),
        #                           tuple([b[2] + ww, b[3] + hh]),
        #                           color_rectangle, 2)
                        
        image = QImage(frame, frame.shape[1], frame.shape[0],
                        frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))
        # img_blank = np.zeros((int(height*2), width*2, 3), np.uint8)
        if self.save_flag==1:
            # for ii in range(height*2):
            #     for jj in range(width*2):
            #         img_blank[ii][jj] = img_rd[d.top()-hh + ii][d.left()-ww + jj]
            ratio=10
            img_blank=frame1[b[1]-ratio:b[3]+ratio,b[0]-ratio:b[2]+ratio,]
            cv2.imwrite(self.current_face_dir + "/img_face_" + str(Face_Register_con.ss_cnt) + ".jpg", img_blank)
            self.save_flag=0
        if self.rec_flag==1:
            if Face_Recognizer_con.get_face_database():
                Face_Recognizer_con.frame_cnt += 1
                Face_Recognizer_con.last_frame_faces_cnt = Face_Recognizer_con.current_frame_face_cnt
                Face_Recognizer_con.current_frame_face_cnt = len(faces)
                if Face_Recognizer_con.current_frame_face_cnt == Face_Recognizer_con.last_frame_faces_cnt:
                    if "unknown" in Face_Recognizer_con.current_frame_name_list:
                        Face_Recognizer_con.reclassify_interval_cnt += 1
                    if Face_Recognizer_con.current_frame_face_cnt ==1:
                        if Face_Recognizer_con.reclassify_interval_cnt==Face_Recognizer_con.reclassify_interval:

                            Face_Recognizer_con.reclassify_interval_cnt=0
                            Face_Recognizer_con.current_frame_face_feature_list = []
                            Face_Recognizer_con.current_frame_face_X_e_distance_list = []
                            Face_Recognizer_con.current_frame_name_list = []

                            for i in range(len(faces)):
                                shape = predictor(frame1, faces[i])
                                Face_Recognizer_con.current_frame_face_feature_list.append(
                                    face_reco_model.compute_face_descriptor(frame1, shape))
                            for k in range(len(faces)):
                                Face_Recognizer_con.current_frame_name_list.append("unknown")

                                # b. 每个捕获人脸的名字坐标 / Positions of faces captured
                                Face_Recognizer_con.current_frame_face_position_list.append(tuple(
                                    [faces[k].left(),
                                     int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

                                # c. 对于某张人脸，遍历所有存储的人脸特征 / For every face detected, compare it with all the faces in the database
                                for i in range(len(Face_Recognizer_con.features_known_list)):
                                    # 如果 person_X 数据不为空 / If the data of person_X is not empty
                                    if str(Face_Recognizer_con.features_known_list[i][0]) != '0.0':
                                        #: ", end='')
                                        e_distance_tmp = Face_Recognizer_con.return_euclidean_distance(
                                            Face_Recognizer_con.current_frame_face_feature_list[k],
                                            Face_Recognizer_con.features_known_list[i])
                                        print(e_distance_tmp)
                                        Face_Recognizer_con.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                                    else:
                                        # 空数据 person_X / For empty data
                                        Face_Recognizer_con.current_frame_face_X_e_distance_list.append(999999999)
                                #print("            >>> current_frame_face_X_e_distance_list:", Face_Recognizer_con.current_frame_face_X_e_distance_list)

                                similar_person_num = Face_Recognizer_con.current_frame_face_X_e_distance_list.index(
                                    min(Face_Recognizer_con.current_frame_face_X_e_distance_list))

                                if min(Face_Recognizer_con.current_frame_face_X_e_distance_list) < 0.4:
                                    # 在这里更改显示的人名 / Modify name if needed
                                    #self.show_chinese_name()
                                    Face_Recognizer_con.current_frame_name_list[k] = Face_Recognizer_con.name_known_list[similar_person_num]
                                    print("            >>> recognition result for face " + str(k + 1) + ": " +
                                          Face_Recognizer_con.name_known_list[similar_person_num])
                                else:
                                    print(
                                        "            >>> recognition result for face " + str(k + 1) + ": " + "unknown")
                        else:
                            #print("   >>> scene 1.2 不需要对于当前帧重新进行人脸识别 / No re-classification for current frame")
                            for k, d in enumerate(faces):
                                Face_Recognizer_con.current_frame_face_position_list[k] = tuple([faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)])
                                frame = Face_Recognizer_con.draw_name(frame)
                else:
                    Face_Recognizer_con.current_frame_face_position_list = []
                    Face_Recognizer_con.current_frame_face_X_e_distance_list = []
                    Face_Recognizer_con.current_frame_face_feature_list = []

                    if Face_Recognizer_con.current_frame_face_cnt == 1:
                        print("   >>> scene 2.1 出现人脸，进行人脸识别 / Get person in this frame and do face recognition")
                        Face_Recognizer_con.current_frame_name_list = []

                        for i in range(len(faces)):
                            shape = predictor(frame, faces[i])
                            Face_Recognizer_con.current_frame_face_feature_list.append(
                                face_reco_model.compute_face_descriptor(frame, shape))
                        for k in range(len(faces)):
                            Face_Recognizer_con.current_frame_name_list.append("unknown")

                            # b. 每个捕获人脸的名字坐标 / Positions of faces captured
                            Face_Recognizer_con.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                            for i in range(len(Face_Recognizer_con.features_known_list)):
                                # 如果 person_X 数据不为空 / If data of person_X is not empty
                                if str(Face_Recognizer_con.features_known_list[i][0]) != '0.0':
                                    #print("            >>> with person", str(i + 1), "the e distance: ", end='')
                                    e_distance_tmp = Face_Recognizer_con.return_euclidean_distance(
                                        Face_Recognizer_con.current_frame_face_feature_list[k],
                                        Face_Recognizer_con.features_known_list[i])
                                    print(e_distance_tmp)
                                    seFace_Recognizer_conlf.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                                else:
                                    # 空数据 person_X / Empty data for person_X
                                    Face_Recognizer_con.current_frame_face_X_e_distance_list.append(999999999)
                            similar_person_num = Face_Recognizer_con.current_frame_face_X_e_distance_list.index(min(Face_Recognizer_con.current_frame_face_X_e_distance_list))

                            if min(Face_Recognizer_con.current_frame_face_X_e_distance_list) < 0.4:
                                #self.show_chinese_name()
                                Face_Recognizer_con.current_frame_name_list[k] = Face_Recognizer_con.name_known_list[similar_person_num]
                                print("            >>> recognition result for face " + str(k + 1) + ": " +
                                      Face_Recognizer_con.name_known_list[similar_person_num])
                            else:
                                print("            >>> recognition result for face " + str(k + 1) + ": " + "unknown")
                        if "unknown" in Face_Recognizer_con.current_frame_name_list:
                            Face_Recognizer_con.reclassify_interval_cnt+=1
                    elif Face_Recognizer_con.current_frame_face_cnt == 0:
                        print("   >>> scene 2.2 人脸消失, 当前帧中没有人脸 / No face in this frame!!!")

                        Face_Recognizer_con.reclassify_interval_cnt=0
                        Face_Recognizer_con.current_frame_name_list = []
                        Face_Recognizer_con.current_frame_face_feature_list = []
            self.result.setText('人脸识别结果为：'+str(Face_Recognizer_con.current_frame_name_list))

    def save_pic(self):
        if self.floader_flag:
            self.save_flag=1
            Face_Register_con.ss_cnt+=1
        else :
            QMessageBox.warning(self,'警告','保存图像前必须先创建对应人脸文件夹')
    def create_floder(self):
        self.rec_flag==0
        self.result.setText('')
        Face_Register_con.check_existing_faces_cnt()
        Face_Register_con.ss_cnt = 0 
        Face_Register_con.existing_faces_cnt +=1
        text, okPressed = QInputDialog.getText(self, "人脸输入","你的名字（请输入英文）:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.name=text
            self.current_face_dir = Face_Register_con.path_photos_from_camera  + str(Face_Register_con.existing_faces_cnt)+"_"+  self.name
            os.makedirs(self.current_face_dir)
            QMessageBox.information(self, '操作成功', '已创建新的人脸库')
            #print(Face_Register_con.existing_faces_cnt)
            self.floader_flag=1
    def delet(self):
        Face_Register_con.pre_work_del_old_face_folders()
        QMessageBox.information(self, '操作成功', '已删除所有人脸数据')
    def feature(self):
        Face_Register_con.check_existing_faces_cnt()
        #print(Face_Register_con.existed_name)
        person_list = os.listdir("data/data_faces_from_camera/")
        person_num_list = []
        for person in person_list:
            person_num_list.append(int(person.split('_')[0]))
        person_cnt = max(person_num_list)

        with open("data/features_all.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for person in range(person_cnt):
                # Get the mean/average features of face/personX, it will be a list with a length of 128D
                print(path_images_from_camera + Face_Register_con.existed_name[person] + str(person + 1))
                features_mean_personX = features_extraction_to_csv.return_features_mean_personX(path_images_from_camera + str(person + 1)+"_" +Face_Register_con.existed_name[person] )
                writer.writerow(features_mean_personX)
                print(" >> 特征均值 / The mean of features:", list(features_mean_personX), '\n')
            print("所有录入人脸数据存入 / Save all the features of faces registered into: data/features_all.csv")
            QMessageBox.information(self, '操作成功', '库中人脸特征已提取')
    def recognize(self):
        self.rec_flag=1
 
if __name__ == "__main__":
    Face_Register_con = get_faces_from_camera.Face_Register()
    Face_Recognizer_con = face_reco_from_camera_ot_single_person.Face_Recognizer()
    retinaface = Retinaface()
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')
    face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")
    color_rectangle = (0, 0, 255)
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())
