from __future__ import print_function

import keras
from keras.callbacks import TensorBoard
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

from tinyenv.flags import flags

FLAGS = flags()

# the data, shuffled and split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

model = Sequential()
model.add(Dense(FLAGS.layer_size, activation=FLAGS.activation,
                input_shape=(784,)))
model.add(Dropout(FLAGS.dropout))
model.add(Dense(FLAGS.layer_size, activation=FLAGS.activation))
model.add(Dropout(FLAGS.dropout))
# Output layer should be 10 node softmax.
model.add(Dense(10, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=FLAGS.batch_size,
                    epochs=FLAGS.epochs,
                    verbose=1,
                    validation_data=(x_test, y_test),
                    callbacks=[TensorBoard(log_dir=FLAGS.log_dir)])
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
