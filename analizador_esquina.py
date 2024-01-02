import cv2

def dibujar_circulo(image_path, coordenada, nuevo_tamano=None):
    # Cargar la imagen
    imagen = cv2.imread(image_path)

    # Convertir la coordenada a enteros
    x, y = map(int, coordenada)

    # Dibujar un círculo en la coordenada especificada
    cv2.circle(imagen, (x, y), 8, (0, 255, 255), -1)  # El último argumento -1 indica que el círculo se rellenará

    if nuevo_tamano is not None:
        imagen = cv2.resize(imagen, nuevo_tamano)

    # Mostrar la imagen con el círculo
    cv2.imshow('Imagen con Círculo', imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Ruta de la imagen
imagen_ruta = 'C:/Users/Peter/Desktop/2023-2/MACHINE LEARNING/Proyecto semestral/Set2/20231126-180000084_id40115361.png'

# Coordenada donde se dibujará el círculo (por ejemplo, (100, 200))
coordenada_circulo = (161, 1470)

# Nuevo tamaño de la imagen (opcional, déjalo como None si no quieres redimensionar)
nuevo_tamano = (1000, 600)  # Modifica según tus necesidades

# Llamar a la función para dibujar el círculo y mostrar la imagen redimensionada
dibujar_circulo(imagen_ruta, coordenada_circulo, nuevo_tamano)