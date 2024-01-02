import tensorflow as tf
from tensorflow.keras import layers, models
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import metrics

# Cargar el conjunto de datos desde el archivo CSVr
data = pd.read_csv(r'C:\Users\Peter\Desktop\2023-2\MACHINE LEARNING\Proyecto semestral\datos.csv', delimiter=";")
#print(data.head())
# Codificar las etiquetas ('esquina' y 'no esquina') a valores numéricos
label_encoder = LabelEncoder() #clase que transforma caracteres en numeros
data['label'] = label_encoder.fit_transform(data['label']) #los datos de label se transforman a datos numericos
data['label'] = 1 - data['label']
data['label'] = data['label'].astype(str) #los datos de label se convierten en str
#print(data.dtypes)
print(data)


# Dividir el conjunto de datos en entrenamiento y prueba
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42) #conjuntos de datos y pruebas

# Crear generadores de datos para cargar las imágenes en lotes
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255) #se normalizan los datos de intensidad de pixel a la escala entre 0 y 1
test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255) #se normalizan los datos de intensidad de pixel a la escala entre 0 y 1

train_generator = train_datagen.flow_from_dataframe(#se cargan imgs a partir de DataFrame de entrenamiento de datos
    train_data,
    x_col='image_path', #rutas de imgs
    y_col='label', #labels
    target_size=(100, 100),  # Ajusta el tamaño según tus necesidades
    batch_size=50, #lotes por cada epoch
    class_mode='binary',  # Si hay solo dos clases
)

test_generator = test_datagen.flow_from_dataframe(#se cargan imgs a partir de DataFrame de prueba de datos
    test_data,
    x_col='image_path',
    y_col='label',
    target_size=(100, 100),
    batch_size=50,
    class_mode='binary',
)

# Construir el modelo de red neuronal
model = models.Sequential() #modelo secuencial
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3))) #1ra capa convolucional
#pars: nro de kernels: 32,  tamaño de kernel: (3,3), no linealidad, tamaño: 100x100 y 3 canales RGB 

model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))#capa final Dense, permite al modelo la clasificacion en el lado positivo

# Compilar el modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[metrics.Recall()])

# Entrenar el modelo
history = model.fit(
    train_generator,
    epochs=250,
    validation_data=test_generator
)

# Evaluar el modelo
test_loss, test_rec = model.evaluate(test_generator)
print(f'rec: {test_rec}')

# Guardar el modelo entrenado para su posterior uso
model.save(r'C:\Users\Peter\Desktop\2023-2\MACHINE LEARNING\Proyecto semestral\cnn.h5')