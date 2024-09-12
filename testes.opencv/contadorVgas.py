import cv2
import mysql.connector
import pickle
import numpy as np

vagas = []

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host="15.228.253.236",
    user="admin",
    password="root",
    database="estacionavagas",
    port=3306
)

cursor = conn.cursor()

# Carrega as coordenadas das vagas a partir do arquivo vagas.pkl
with open('vagas.pkl', 'rb') as arquivos:
    vagas = pickle.load(arquivos)

# Captura de vídeo
video = cv2.VideoCapture('inovatech/video.mp4')

while True:
    check, img = video.read()
    if not check:
        break
    
    imgcinza = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgTr = cv2.adaptiveThreshold(imgcinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgTr, 5)
    kernel = np.ones((3, 3), np.int8)
    imgdilat = cv2.dilate(imgMedian, kernel)

    # Loop para processar cada vaga
    for i, (x, y, w, h) in enumerate(vagas):
        vaga = imgdilat[y:y + h, x:x + w]
        count = cv2.countNonZero(vaga)
        cv2.putText(img, str(count), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if count < 900:
            status = 'Livre'
            color = (0, 255, 0)  # Verde para vagas livres
        else:
            status = 'Ocupada'
            color = (0, 0, 255)  # Vermelho para vagas ocupadas

        # Inserir ou atualizar o status da vaga no banco de dados
        cursor.execute("""
            INSERT INTO vagas_livres (spot_number, status)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """, (i + 1, status))

        # Desenhar a caixa da vaga no vídeo
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

    conn.commit()
    cv2.imshow('video', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

conn.close()
video.release()
cv2.destroyAllWindows()
