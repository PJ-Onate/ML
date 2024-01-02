import os
import csv
import cv2
import numpy as np

i = 1
def obtener_esquinas(image_path, radio_circulo=15, paso_circulo=10):
    global i
    lista = []
    old_frame = cv2.imread(image_path)
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(old_gray, 15)
    gauss = cv2.GaussianBlur(median, (5, 5), 0)
    dst = cv2.cornerHarris(gauss, 5, 7, 0.01)
    
    # Threshold para seleccionar esquinas
    umbral_harris = 0.01 * dst.max()
    coordenadas_esquinas = np.where(dst > umbral_harris)

    for corner_y, corner_x in zip(coordenadas_esquinas[0], coordenadas_esquinas[1]):
        a = int(corner_x)
        b = int(corner_y)
        
        # Dibuja un círculo solo cada paso_circulo píxeles
        if a % paso_circulo == 0 and b % paso_circulo == 0:
            cv2.circle(old_frame, (a, b), 8, 255, -1)
            
            if 0 <= a < old_frame.shape[0] and 0 <= b < old_frame.shape[1]:
                # Calcular el centro de masa de los píxeles de la esquina
                moments = cv2.moments(gauss[b:b+tamano_roi[0], a:a+tamano_roi[1]])
                
                # Verificar que el momento central no sea cero
                if moments["m00"] != 0:
                    centro_x = int(moments['m10'] / moments['m00'])
                    centro_y = int(moments['m01'] / moments['m00'])

                    # Extraer la región de interés (ROI) de la imagen
                    roi = old_frame[a:a + tamano_roi[0], b:b + tamano_roi[1]]

                    # Verificar que la ROI no esté vacía
                    if roi.size > 0:
                        # Guardar la ROI como una imagen separada (opcional)
                        nombre_archivo = str(i) + f'roi_{centro_x}_{centro_y}.jpg'
                        lista.append(((centro_x, centro_y), roi, nombre_archivo))
                        i = i+1
    return old_frame, lista

dataset_folder = 'C:/Users/Peter/Desktop/2023-2/MACHINE LEARNING/Proyecto semestral/Set2'
csv_file_path = 'C:/Users/Peter/Desktop/2023-2/MACHINE LEARNING/Proyecto semestral/datos.csv'

tamano_roi = (50, 50)

with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    header = ['image_path', 'corner_x', 'corner_y']
    csv_writer.writerow(header)

    for image_file in os.listdir(dataset_folder):
        image_path = os.path.join(dataset_folder, image_file)
        imagen, rois = obtener_esquinas(image_path)
        
        for roi in rois:
            (centro_x, centro_y), _, _ = roi
            csv_writer.writerow([image_path, centro_x, centro_y])
            
        cv2.imwrite(os.path.join('C:/Users/Peter/Desktop/2023-2/MACHINE LEARNING/Proyecto semestral', f'{image_file}_output.jpg'), imagen)

print(f'Se ha creado el archivo CSV en: {csv_file_path}')

