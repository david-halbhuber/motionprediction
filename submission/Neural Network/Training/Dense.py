# Python file for training the Dense Model
# Change Prediciton Value by changing "PREDICITON_VALUE_IN_FRAMES"



from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
import logging
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
from keras.backend.tensorflow_backend import set_session



set_session(session)

# Define the path to the trainingset
df = pd.read_csv(r"PATH_TO_TRAINING_SET", header=None)

# Define the prediciton value in frames (1 Frame = 4ms, 25 Frames = 100ms)
PREDICITION_VALUE_IN_FRAMES = 50

# Train, test Split 9:1 Ration
TRAIN_SPLIT = 0.9
START_FRAME = 1

# Config from Florin Schwappach regarding gpu usage on the ML-Server
config = tf.ConfigProto()
CUDA_VISIBLE_DEVICES=""
config.gpu_options.allow_growth = True
session = tf.InteractiveSession(config=config)
set_session(session)

# Which values from the dataset do you want to use? 
# 87 coresponds to using everthing except fingers
# 207 also trains finger values
INPUT_PREDICITION_VALUE = 87
PREDICITION_SPLIT_JOINTS_VALUE = 87

# Define with which prefix should be saved before ES
prefix = 'MODEL_PREFIX'


#Define the actual model checkpoint
path_checkpoint = 'MODEL_NAME_TO_SAVE.keras'


callback_checkpoint = ModelCheckpoint(filepath=path_checkpoint,
                                      monitor='val_loss',
                                      verbose=1,
                                      save_weights_only=False,
                                      save_best_only=True)

callback_early_stopping = EarlyStopping(monitor='val_loss',
                                        patience=2, verbose=1)

callback_tensorboard = TensorBoard(log_dir='./23_logs/',
                                   histogram_freq=0,
                                   write_graph=False)

callback_reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                       factor=0.1,
                                       min_lr=1e-5,
                                       patience=2,
                                       verbose=1)

callbacks = [callback_checkpoint,
             callback_tensorboard,
             callback_reduce_lr]



# Change the range of for if you want to concate multiple datasets
# Not needed if final data set is used for train
#for i in range(1,2):
df = df.drop(df.columns[87:], axis=1)
df_target = df.shift(-PREDICITION_VALUE_IN_FRAMES)






df = df.iloc[1:]
df_target = df_target.iloc[1:]


print(df.head())
print(df_target.head())

# Removing prediciton value from end of dfs
x_data = df.values[0:-PREDICITION_VALUE_IN_FRAMES]
y_data = df_target.values[:-PREDICITION_VALUE_IN_FRAMES]

#df = df[:-PREDICITION_VALUE_IN_FRAMES]
#df_target = df_target[:-PREDICITION_VALUE_IN_FRAMES]






# Splitting into train and test set 
num_data = len(x_data)
num_train = int(TRAIN_SPLIT*num_data)
num_test = num_data - num_train

print("Training on :", num_train, " Samples. Testing on : ", num_test, " Samples.")

# Splitting into X,Y
x_train = x_data[0:num_train]
x_test = x_data[num_train:]

y_train = y_data[0:num_train]
y_test = y_data[num_train:]

# Scaling the data to be easier handle by the RNN
# Initianig a new scaler-object for x scaling


num_x_signals = x_data.shape[1]
num_y_signals = y_data.shape[1]

l1 = tf.keras.layers.Dense(units=INPUT_PREDICITION_VALUE, input_shape=[INPUT_PREDICITION_VALUE,])
l3 = tf.keras.layers.Dense(units=2048)
l4 = tf.keras.layers.Dense(units=4096, activation="relu")
l5 = tf.keras.layers.Dropout(0.1)
l7 = tf.keras.layers.Dense(units=PREDICITION_SPLIT_JOINTS_VALUE)
model = tf.keras.Sequential([l1,l3,l4,l7])
model.compile(loss='mean_squared_error',metrics=['accuracy'],
            optimizer=tf.keras.optimizers.Adam(lr=1e-4))
model.summary()
history = model.fit(x_train,
        y_train,
        epochs=50,
        batch_size=512,
        validation_data=(x_test, y_test), callbacks=callbacks)
print("Finished")
plt.xlabel('Epoch Number')
plt.ylabel("Accuracy")
plt.plot(history.history['acc'])
plt.plot(history.history['loss'])

model.save(prefix)

print("Model predicition: ", model.predict(df.iloc[0:1]))
print("Actual value: ",df_target.iloc[0:1])
    

    

