from __future__ import absolute_import, division, print_function

import tensorflow as tf
from tensorflow import keras

import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

import os

# Read in data, shuffle
df = pd.read_csv("data.csv")
df.sample(frac=1)

# Split data into features and labels
Y = df["time"].values.reshape(df.shape[0], 1)
df = df.drop("time", 1)
df = df.drop("bus_id", 1)
dataset = df.values
dataset = dataset.astype(float)
X = dataset[:, 1:dataset.shape[1]]

# Split into training and test groups
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

# feature normalization
mean = X_train.mean(axis=0)
std = X_train.std(axis=0)
X_train = (X_train - mean) / std
X_test = (X_test - mean) / std


# Defines the model
def build_model():
    model = keras.Sequential([
        keras.layers.Dense(64, activation=tf.nn.relu,
                           input_shape=(X_train.shape[1],)),
        keras.layers.Dense(64, activation=tf.nn.relu),
        keras.layers.Dense(1)
    ])

    optimizer = tf.train.RMSPropOptimizer(0.001)

    model.compile(loss="mse",
                  optimizer=optimizer,
                  metrics=["mae"])
    return model

# Uses the model
model = build_model()
early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=20)


# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0:
            print("")
        print(".", end="")

EPOCHS = 2500

# Saves the things
checkpoint_path = "./checkpoint.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callbacks = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                   save_weights_only=True,
                                   verbose=1, period=EPOCHS)

# Store training stats
history = model.fit(X_train, Y_train, epochs=EPOCHS,
                    validation_split=0.2, verbose=0,
                    callbacks=[PrintDot(), cp_callbacks])

# Graph training and cross validation losses
import matplotlib.pyplot as plt

plt.figure()
plt.xlabel('Epoch')
plt.ylabel('Mean Abs Error')
plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),
         label='Train Loss')
plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),
         label='Val loss')
plt.legend()
plt.xlim(plt.xlim())
plt.ylim(plt.ylim())
plt.show()

# Runs test points through algorithm & predicts outcome
test_predictions = model.predict(X_test).flatten()

plt.scatter(Y_test, test_predictions)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.axis('equal')
plt.xlim(plt.xlim())
plt.ylim(plt.ylim())
_ = plt.plot([-100, 100], [-100, 100])
plt.show()


error = test_predictions - Y_test
plt.hist(error, bins=50)
plt.xlabel("Prediction Error")
_ = plt.ylabel("Count")
plt.show()
