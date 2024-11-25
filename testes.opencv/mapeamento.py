import cv2 
import pickle

img = cv2.imread('./img/estacionamentos.jpg')
print(f'Tamanho da imagem: {img.shape[1]}x{img.shape[0]} (Largura x Altura em pixels)')
vagas = []
for x in range(22):
    vaga = cv2.selectROI('vagas',img,False)
    cv2.destroyWindow('vagas')
    vagas.append(vaga)


    for x,y,w,h in vagas:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)


with open('vagas.pkl','wb')as arquivos:
    pickle.dump(vagas,arquivos)


print(vagas)