import os
import csv
import cv2
import numpy as np

i=1
def obtener_esquinas(image_path):
    global i
    lista = []
    old_frame = cv2.imread(image_path)
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(old_gray, 15)
    gauss = cv2.GaussianBlur(median, (5, 5), 0)
    dst = cv2.cornerHarris(gauss, 64, 31, 0.21)
    # Threshold para seleccionar esquinas
    umbral_harris = 0.01 * dst.max()
    coordenadas_esquinas = np.where(dst > umbral_harris)
    print(coordenadas_esquinas)

    for corner_y, corner_x in zip(coordenadas_esquinas[0], coordenadas_esquinas[1]):
        a = int(corner_x)
        b = int(corner_y)
        cv2.circle(old_frame, (a, b), 15, 255, -1)
        if 0 <= a < old_frame.shape[0] and 0 <= b < old_frame.shape[1]:
            # Extraer la región de interés (ROI) de la imagen
            roi = old_frame[a:a + tamano_roi[0], b:b + tamano_roi[1]]

            # Verificar que la ROI no esté vacía
            if roi.size>0:
                # Guardar la ROI como una imagen separada (opcional)
                nombre_archivo = str(i)+f'roi_{a}_{b}.jpg'
                #cv2.imwrite(nombre_archivo, roi)
                lista.append(((a,b), roi, nombre_archivo))
    return old_frame, lista

dataset_folder = 'C:/Users/Peter/Desktop/2023-2/MACHINE LEARNING/Proyecto semestral/Set2'
csv_file_path = 'C:/Users/Peter/Desktop/2023-2/MACHINE LEARNING/Proyecto semestral/datos.csv'

# Abre el archivo CSV en modo de escritura
tamano_roi = (50, 50)
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Define los encabezados: image_path, corner_x, corner_y
    header = ['image_path', 'corner_x', 'corner_y']
    csv_writer.writerow(header)

    # Itera sobre las imágenes en la carpeta
    for image_file in os.listdir(dataset_folder):
        image_path = os.path.join(dataset_folder, image_file)
    
        # Obtén las coordenadas de las esquinas
        imagen, rois = obtener_esquinas(image_path)

        # Escribe una nueva fila en el archivo CSV por cada tupla de coordenadas
        for roi in rois:
            x, y = roi[0]
            csv_writer.writerow([image_path, x, y])
            cv2.circle(imagen, (x, y), 15, 255, -1)
    #    i = i+1
        cv2.imwrite(os.path.join('C:/Users/Peter/Desktop/2023-2/MACHINE LEARNING/Proyecto semestral', f'{image_file}_output.jpg'), imagen)

print(f'Se ha creado el archivo CSV en: {csv_file_path}')



