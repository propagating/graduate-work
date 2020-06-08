import pandas as pd
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 784)  # 28*28=784
x_test = x_test.reshape(-1, 784)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
# 128 images in each batch
batch_size = 128
# 0-9 numbered images
num_classes = 10
# train for 20 epochs
epochs = 20

# Scale the data to be between 0 and 1
x_train /= 255.
x_test /= 255.

print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors (one hot encoding)
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

print(y_train.shape, 'y_train')
print(y_test.shape, 'y_test')
# start building the model
sgdNN = Sequential()

# add a fully connected hidden layer
sgdNN.add(Dense(16, activation='relu', input_shape=(784,)))

# add another fully connected hidden layer
sgdNN.add(Dense(16, activation='relu'))

# add last layer with activation for classification
sgdNN.add(Dense(num_classes, activation='softmax'))
sgdNN.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy'])
sgdNN.summary()

history = sgdNN.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(x_test, y_test))
weights = []

for layer in sgdNN.layers:
    weights.append(layer.get_weights())

np.array(weights[0][0]).shape

w1 = np.array(weights[0][0]).reshape(16, 28, 28)

fig, axs = plt.subplots(4, 4, figsize=(10, 10))
for j in range(4):
    for k in range(4):
        i = j * 4 + k
        axs[j, k].imshow(w1[i, :, :])
