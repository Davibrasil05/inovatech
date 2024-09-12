import cv2
import pickle
import numpy as np
vagas = []


with open('vagas.pkl','rb')as arquivos:
    vagas = pickle.load(arquivos)


video =cv2.VideoCapture('./videos/maquete06.mp4')

while True:
    check,img = video.read()
    imgcinza= cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    imgTr = cv2.adaptiveThreshold(imgcinza,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgMedian= cv2.medianBlur(imgTr,5)
    kernel =np.ones((3,3,),np.int8)
    imgdilat= cv2.dilate(imgMedian,kernel)


    for x,y,w,h in vagas :
        vaga= imgdilat[y:y+h,x:x+w]
        count= cv2.countNonZero(vaga)
        cv2.putText(img,str(count),(x,y+h-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
        cv2.rectangle(img,(x,y), (x+w,y+h),(255,0,0),1)

        if count < 900:
             cv2.rectangle(img,(x,y), (x+w,y+h),(0,255,0),1)
        else:
             cv2.rectangle(img,(x,y), (x+w,y+h),(0,0,255),1)

    cv2.imshow('video',img)
    #cv2.imshow('videoth',imgdilat)
    cv2.waitKey(10)
