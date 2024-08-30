import cv2
camera = cv2.VideoCapture(0)
classificador = cv2.CascadeClassifier(r'inovatech/haarcascade_frontalface_default.xml')

while True :
    check,img= camera.read()
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    objetos = classificador.detectMultiScale(imgGray,minSize=(100,100))#vai detectar onde está o rosto em cordenadas 

    for x,y,l,a in objetos:#pegamos as variaveis x y l a para as cordenadas e iteramos com o for para objetos que é onde retorna as cordenadas
        cv2.rectangle(img,(x,y),(x+l,y+a),(255,0,0),2)

    cv2.imshow('imagem',img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == 27:  
        break