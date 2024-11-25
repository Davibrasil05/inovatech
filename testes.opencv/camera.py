import cv2

# URL fornecido pelo aplicativo de câmera IP
url = "http://192.168.59.49:8080/video"

# Inicia a captura de vídeo
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Exibe o vídeo em tempo real
    cv2.imshow("Câmera do Celular", frame)
    
    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
