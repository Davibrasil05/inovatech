import cv2
import mysql.connector
import pickle
import numpy as np

vagas = []

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vagas",
)

cursor = conn.cursor()

# Carrega as coordenadas das vagas a partir do arquivo vagas.pkl
with open('vagas.pkl', 'rb') as arquivos:
    vagas = pickle.load(arquivos)

# Utilize a câmera ou stream ao vivo
video = cv2.VideoCapture('http://172.20.10.3:8080/video')  # Substitua pelo URL da câmera

while True:
    check, img = video.read()
    if not check:
        print("Erro ao capturar frame ou conexão encerrada.")
        break

    # Pré-processamento da imagem
    imgcinza = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgTr = cv2.adaptiveThreshold(imgcinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgTr, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgdilat = cv2.dilate(imgMedian, kernel)

    # Lista para armazenar logs e possíveis dados para o banco
    dados_vagas = []

    # Loop para processar cada vaga
    for i, (x, y, w, h) in enumerate(vagas):
        vaga = imgdilat[y:y + h, x:x + w]
        count = cv2.countNonZero(vaga)  # Contagem de pixels não zero
        cv2.putText(img, str(count), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Determinar o status da vaga
        if count < 900:
            status = 'Livre'
            color = (0, 255, 0)  # Verde para vagas livres
        else:
            status = 'Ocupada'
            color = (0, 0, 255)  # Vermelho para vagas ocupadas

        # Exibe os dados processados no console (diagnóstico)
        print(f"Vaga {i + 1}: count = {count}, status = {status}")

        # Adiciona os dados da vaga no banco de dados
        cursor.execute("""
            INSERT INTO vagas_livres (spot_number, status)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """, (i + 1, status))

        print(f"Atualizado vaga {i + 1} no banco de dados com status {status}.")

        # Desenhar a caixa da vaga no vídeo
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

    # Salva as alterações no banco de dados
    conn.commit()
    print("Alterações salvas no banco de dados.")

    # Exibição do vídeo
    cv2.imshow('Câmera', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Encerrar conexão com o banco e liberar recursos do OpenCV
conn.close()
video.release()
cv2.destroyAllWindows()
