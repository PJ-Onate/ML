from keras.preprocessing import image
import numpy as np

# Cargar una nueva imagen para la predicción (reemplaza 'ruta_de_la_imagen.jpg')
img_path = 'ruta_de_la_imagen.jpg'
img = image.load_img(img_path, target_size=(altura, ancho))  # Ajusta el tamaño según tu modelo
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0  # Normalizar los valores de píxeles al rango [0, 1]

# Hacer la predicción
predictions = model.predict(img_array)

# Interpreta las predicciones según tu problema específico
print(predictions)