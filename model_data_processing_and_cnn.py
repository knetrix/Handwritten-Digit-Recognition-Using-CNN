"""
The code creates a convolutional neural network model for image classification using the MNIST
dataset and trains it, then evaluates its success rate and displays its summary.
:return: The function `model()` returns a compiled Keras model for image classification.
"""
from keras import utils
from keras.datasets import mnist
from keras.layers import Activation, Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from keras.models import Sequential

# Load the MNIST Dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype("float32")
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype("float32")

X_train = X_train / 255
X_test = X_test / 255

y_train = utils.to_categorical(y_train)
y_test = utils.to_categorical(y_test)

class_number = y_test.shape[1]


def model():
    """
    The Function `model()` Creates a Convolutional Neural Network Model for Image Classification.
    :return: A Compiled Keras Model.
    """

    cnn_model = Sequential()
    cnn_model.add(Conv2D(30, (5, 5), input_shape=(28, 28, 1)))
    cnn_model.add(Activation("relu"))
    cnn_model.add(MaxPooling2D())
    cnn_model.add(Conv2D(15, (3, 3)))
    cnn_model.add(Activation("relu"))
    cnn_model.add(MaxPooling2D())

    cnn_model.add(Flatten())
    cnn_model.add(Dense(375))
    cnn_model.add(Activation("relu"))
    cnn_model.add(Dropout(0.3))
    cnn_model.add(Dense(150))
    cnn_model.add(Activation("relu"))
    cnn_model.add(Dropout(0.1))
    cnn_model.add(Dense(class_number, activation="softmax"))

    cnn_model.compile(
        loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )
    return cnn_model


model = model()

# Training The Model with MNIST Dataset
model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=20,
    batch_size=150,
    shuffle=True,
)
model.save("mnist_model.h5")

# I Test The Model with MNIST Test Data and Measure Success Rate
scores = model.evaluate(X_test, y_test, verbose=0)
print(f"Success Rate:  {scores[1] * 100:.2f}")

# General Structure of The Model
utils.plot_model(model, "model.png", show_shapes=True)

model.summary()
