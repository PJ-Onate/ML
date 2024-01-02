from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from keras.models import load_model
import cv2

ruta_model= r'resnet.h5'
model= load_model(ruta_model)


# Cargar la imagen
img_path = r'SetImages\20230628-005500170_id40115361.png'
img = cv2.imread(img_path)

old_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
median = cv2.medianBlur(old_gray, 15)
gauss = cv2.GaussianBlur(median, (5, 5), 0)
dst = cv2.cornerHarris(gauss, 64, 31, 0.21)
dst = cv2.dilate(dst, None)

# Apply threshold
ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
dst = np.uint8(dst)

# Connected components
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.3)
corners = cv2.cornerSubPix(gauss, np.float32(centroids), (5, 5), (-1, -1), criteria)

# Tamaño de la región de interés (ROI)
roi_size = (100, 100)

# Umbral para clasificar
umbral = 0.5

lista = []
i = 1

# Iterar sobre las esquinas
for corner_x, corner_y in corners:
    # Extraer la región de interés (ROI) de la imagen
    corner_x, corner_y = int(corner_x), int(corner_y)
    center_x = corner_x
    center_y = corner_y

    if (corner_x - roi_size[0] // 2 > 0) and (corner_x + roi_size[0] // 2 < img.shape[1]) and \
        (corner_y - roi_size[1] // 2 > 0) and (corner_y + roi_size[1] // 2 < img.shape[0]):

        # Extraer la región de interés (ROI) con la esquina en el centro
        roi = img[
            center_y - roi_size[1] // 2 : center_y + roi_size[1] // 2,
            center_x - roi_size[0] // 2 : center_x + roi_size[0] // 2
        ]

        # Verificar que la ROI no esté vacía
        if roi.size > 0:
            # Guardar la ROI como una imagen separada (opcional)
            nombre_archivo = f"roi_{corner_x}_{corner_y}.jpg"
            

            # Agregar la información al DataFrame (si es necesario)
            # data = data.append({
            #     'image_path': nombre_archivo,
            #     'corner_x': corner_x,  # Usar las coordenadas del centro
            #     'corner_y': corner_y,  # Usar las coordenadas del centro
            #     'label': 'esquina'  # Puedes etiquetar manualmente cada ROI
            # }, ignore_index=True)

            roi_array = cv2.resize(roi, (100, 100))  # Redimensionar a la forma esperada
            cv2.imwrite(nombre_archivo, roi_array)
            roi_array = np.expand_dims(roi_array, axis=0)  # Agregar la dimensión del lote (batch dimension)
            roi_array = roi_array.astype('float32') 
            roi_array /= 255.1

            # Realizar la predicción
            prediction_1 = model.predict(roi_array)

            # Clasificar según el umbral
            if prediction_1 and len(prediction_1) > 0 and len(prediction_1[0]) > 0:
                probabilidad_esquina = prediction_1[0][0]
                print(f"Probabilidad de que la esquina en ({corner_x}, {corner_y}) sea 'esquina': {probabilidad_esquina}")

                # Clasificar según el umbral
                if probabilidad_esquina > umbral:
                    print(f"La esquina en ({corner_x}, {corner_y}) es clasificada como 'esquina'.")
                    cv2.circle(img, (corner_x, corner_y), 8, (0, 255, 255), -1)
                else:
                    print(f"La esquina en ({corner_x}, {corner_y}) no es clasificada como 'esquina'.")
        i += 1


nuevo_tamano = (1000, 600)

# Redimensionar la imagen
img = cv2.resize(img, nuevo_tamano)
#img_vgg16 = cv2.resize(img_vgg16, nuevo_tamano)
cv2.imshow("img_cnn", img)
#cv2.imshow("img_vgg16", img_vgg16)
cv2.waitKey(0)


