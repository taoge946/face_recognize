import cv2
a=cv2.imread('F:/python/ma1.jpg',1)
b=cv2.resize(a,(int(a.shape[1]/3),int(a.shape[0]/3)))
c=cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
face_cascade=cv2.CascadeClassifier(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
faces=face_cascade.detectMultiScale(c,scaleFactor=1.05,minNeighbors=5)
for x,y,w,h in faces:
  b=cv2.rectangle(b,(x,y),(x+w,y+h),(0,255,0),3)
cv2.imshow('handsome boy',b)
k=cv2.waitKey(0)
if(k==27):
    cv2.destroyAllWindows()
elif(k==115):
    cv2.imwrite('F:/python/ma2.jpg',b)
    cv2.destroyAllWindows()