import os
import cv2
import numpy as np
import pandas as pd

# Ruta de la carpeta que contiene las imágenes
carpeta_imagenes = 'Set2'

# Obtener la lista de archivos en la carpeta
archivos_en_carpeta = os.listdir(carpeta_imagenes)

# Filtrar solo los archivos de imagen (puedes ajustar las extensiones según tus necesidades)
archivos_imagenes = [archivo for archivo in archivos_en_carpeta if archivo.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Crear un DataFrame de Pandas para el dataset
data = pd.DataFrame(columns=['image_path', 'corner_x', 'corner_y', 'label'])
# Iterar sobre cada imagen
i=1
for nombre_imagen in archivos_imagenes:
    # Construir la ruta completa de la imagen
    ruta_imagen = os.path.join(carpeta_imagenes, nombre_imagen)
    print(f"Procesando la imagen: {ruta_imagen}")

    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)

    # Convertir la imagen a escala de grises
    old_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(old_gray, 15)
    gauss = cv2.GaussianBlur(median, (5, 5), 0)

    # Aplicar cv2.cornerHarris
    dst = cv2.cornerHarris(gauss, 64, 31, 0.21)
    dst = cv2.dilate(dst, None)

    # Apply threshold
    ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
    dst = np.uint8(dst)

    # Connected components
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.3)
    corners = cv2.cornerSubPix(gauss, np.float32(centroids), (5, 5), (-1, -1), criteria)

    # Tamaño de las ROI
    tamano_roi = (100, 100)
    for corner in corners:
        x,y = corner
        x = int(x)
        y = int(y)
        # Dibujar un círculo en el centro de la esquina
        #cv2.circle(imagen, (x,y), 15, 255, -1)
        print(i, x, y)


    # Iterar sobre las esquinas detectadas y crear las ROI
    for corner_x, corner_y in corners:
        corner_x, corner_y = int(corner_x), int(corner_y)

        # Calcular las coordenadas del centro de la esquina
        center_x = corner_x
        center_y = corner_y    
        if (corner_x - tamano_roi[0] // 2 > 0) and (corner_x + tamano_roi[0] // 2 < imagen.shape[1]) and \
            (corner_y - tamano_roi[1] // 2 > 0) and (corner_y + tamano_roi[1] // 2 < imagen.shape[0]):

                # Extraer la región de interés (ROI) con la esquina en el centro
                roi = imagen[center_y - tamano_roi[1] // 2:center_y + tamano_roi[1] // 2,
                            center_x - tamano_roi[0] // 2:center_x + tamano_roi[0] // 2]

                # Verificar que la ROI no esté vacía
                if roi.size > 0:
                    # Guardar la ROI como una imagen separada (opcional)
                    nombre_archivo = 'ROIS/'+str(i) + f'roi_{corner_x}_{corner_y}.jpg'
                    cv2.imwrite(nombre_archivo, roi)

                    # Agregar la información al DataFrame
                    data = data.append({
                        'image_path': nombre_archivo,
                        'corner_x': corner_x,  # Usar las coordenadas del centro
                        'corner_y': corner_y,  # Usar las coordenadas del centro
                        'label': 'esquina'  # Puedes etiquetar manualmente cada ROI
                    }, ignore_index=True)
        else:
            # Calcular un tamaño más pequeño para la ROI cerca de los bordes
            # Calcular un tamaño más pequeño para la ROI cerca de los bordes
            tamano_roi_pequeno_x = min(abs(imagen.shape[0] - corner_x), corner_x) 
            tamano_roi_pequeno_y = min(abs(imagen.shape[1] - corner_y), corner_y)
            print(abs(imagen.shape[1] - corner_y), corner_y)
            print("OJO: " + str(corner_x) + " "+ str(corner_y) + ", " + str(tamano_roi_pequeno_x)+ " " + str(tamano_roi_pequeno_y))
            # Extraer la región de interés (ROI) más pequeña
            roi = imagen[corner_y - tamano_roi_pequeno_y // 2:corner_y + tamano_roi_pequeno_y // 2,
                        corner_x - tamano_roi_pequeno_x // 2:corner_x + tamano_roi_pequeno_x // 2]
            nombre_archivo = 'ROIS'+str(i) + f'roi_{corner_x}_{corner_y}.jpg'
            data = data.append({
                'image_path': nombre_archivo,
                'corner_x': corner_x,  # Usar las coordenadas del centro
                'corner_y': corner_y,  # Usar las coordenadas del centro
                'label': 'no esquina'  # Puedes etiquetar manualmente cada ROI
            }, ignore_index=True)
    # Guardar la imagen con círculos en el centro de las esquinas
    cv2.imwrite(carpeta_imagenes + str(i) + ".png", imagen)
    i = i + 1


# Guardar el DataFrame como un archivo CSV
data.to_csv('dataset.csv', index=False)
