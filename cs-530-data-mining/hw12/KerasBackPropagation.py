import keras
import seaborn as sns
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD

sns.set()
batch_size = 64
num_classes = 10
epochs = 20

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(-1, 784)
x_test = x_test.reshape(-1, 784)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

x_train /= 255.
x_test /= 255.

print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

print(y_train.shape, 'y_train')
print(y_test.shape, 'y_test')

model = Sequential()
model.add(Dense(16, activation='relu', input_shape=(784,)))
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer=SGD(),
    metrics=['accuracy'])

history = model.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(x_test, y_test))

history.history['epochs'] = range(epochs)

sns.lineplot(x='epochs', y='accuracy', data=history.history, label='Accuracy')
sns.lineplot(x='epochs', y='val_accuracy', data=history.history, label='Val Accuracy')

plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

weights = []
for layer in model.layers:
    weights.append(layer.get_weights())

for i in range(weights[0][0].shape[1]):
    firstLayerImage = weights[0][0][:, i].reshape((28, 28))
    plt.imshow(firstLayerImage)
    plt.show()

for i in range(weights[1][0].shape[1]):
    secondLayerImage = weights[1][0][:, i].reshape((4, 4))
    plt.imshow(secondLayerImage)
    plt.show()

for i in range(weights[2][0].shape[1]):
    thirdLayerImage = weights[2][0][:, i].reshape((4, 4))
    plt.imshow(thirdLayerImage)
    plt.show()
