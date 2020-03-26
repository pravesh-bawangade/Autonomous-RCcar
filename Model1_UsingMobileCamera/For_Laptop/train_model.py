import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np
from sklearn.model_selection import train_test_split
import time


class CNN:

    def __init__(self):
        self.batch_size = 128
        self.num_classes = 3
        self.epochs = 12
        self.model = None

    @staticmethod
    def load_data(input_size, file):
        # input size =(240,320)
        X = np.empty((0, input_size[0] * input_size[1]))
        y = np.empty((0, 3))
        with np.load(file) as data:
            train = data['train']
            train_labels = data['train_labels']
        X = np.vstack((X, train))
        y = np.vstack((y, train_labels))
        return train_test_split(X, y, test_size=0.3)

    def train(self, input_size, file):

        img_rows, img_cols = input_size[0], input_size[1]
        # the data, split between train and test sets
        (x_train, y_train), (x_test, y_test) = self.load_data(input_size, file)

        if K.image_data_format() == 'channels_first':
            x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
            x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
            input_shape = (1, img_rows, img_cols)
        else:
            x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
            x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
            input_shape = (img_rows, img_cols, 1)

        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255
        print('x_train shape:', x_train.shape)
        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')
        """
         # convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)
        """

        self.model = Sequential()
        self.model.add(Conv2D(32, kernel_size=(3, 3),
                              activation='relu',
                              input_shape=input_shape))
        self.model.add(Conv2D(64, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        self.model.add(Flatten())
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(self.num_classes, activation='softmax'))

        self.model.compile(loss=keras.losses.categorical_crossentropy,
                           optimizer=keras.optimizers.Adadelta(),
                           metrics=['accuracy'])

        self.model.fit(x_train, y_train,
                       batch_size=self.batch_size,
                       epochs=self.epochs,
                       verbose=1,
                       validation_data=(x_test, y_test))
        score = self.model.evaluate(x_test, y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        self.model.save(str(time.time()) + "model.h5")

    def predict(self, X):
        out = None
        try:
            _, out = self.model.predict(X)
        except Exception as e:
            print(e)
        return out.argmax(-1)
