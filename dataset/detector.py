import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from keras.optimizers import Adam

# Tamaño de las imágenes de entrada
input_shape = (224, 224, 3)  # Ajusta el tamaño según tus necesidades

# Crear el modelo de red neuronal
model = models.Sequential()

# Capas convolucionales y de pooling
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Flatten para la capa densa
model.add(layers.Flatten())

# Capas densas (totalmente conectadas)
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dropout(0.5))  # Para evitar el sobreajuste
model.add(layers.Dense(1, activation='sigmoid'))  # Salida binaria (esquina o no esquina)

# Compilar el modelo
model.compile(optimizer=Adam(learning_rate=0.001), 
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Mostrar la arquitectura del modelo
model.summary()