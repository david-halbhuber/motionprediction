import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
import os

from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Input, Dense, GRU, Embedding, CuDNNGRU, CuDNNLSTM, Dropout, Flatten
from tensorflow.python.keras.optimizers import RMSprop
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from keras.utils import multi_gpu_model
from keras.backend.tensorflow_backend import set_session


config = tf.ConfigProto()
CUDA_VISIBLE_DEVICES=""
config.gpu_options.allow_growth = True
session = tf.InteractiveSession(config=config)
set_session(session)

# CONSTANTS
# This constant sets the prediciton frame value
# How many frames in the future do you want to predict? 1 = 1 Frame = 4 ms 
# Based on PREDICITON_VALUES_IN_FRAMES is the target df (Y-Output) created. 
PREDICITION_VALUE_IN_FRAMES = 12

PREDICITION_SPLIT_JOINTS_VALUE = 3 

prefix = 'models/87JointsScaled'

# Splitting 90/10 Train/test
TRAIN_SPLIT = 0.9

# Definig the starting Frame 
START_FRAME = 1

# VARS for NN
batch_size = 12
sequence_length = 5
lr = 1e-4

optimizer = tf.keras.optimizers.Adam(lr=lr)



# Keras callbacks
# Implementing Checkpoints for model saving, saving weights, saving only best
# Implementing EarlyStopping 
## EarlyStopping decreases the lr if the val_loss did not decrease for 5 epochs
# Implementing Tensorboard
# Implementing ReduceLROnPLateu Callback
## This callback reduces the LR if the val_loss did not decrease for 2 epochs 
## LR gets reduce by 1e-6
## This is similar to a lr decay 
# 
# 
# ALL CALLBACKS ARE NON VERBOSE, SEE CONSOLE FOR LOGS 
path_checkpoint = 'LSTM_23_1_checkpoint.keras'
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

callbacks = [callback_early_stopping,
             callback_checkpoint,
             callback_tensorboard,
             callback_reduce_lr]


#callbacks = [callback_early_stopping, callback_checkpoint, callback_tensorboard, callback_reduce_lr]

df = pd.read_csv(r"finalData/df_1_TO_8.csv", header=None)





# Creating target df, by shifting new dataframe to prediciton value in frames



# Only use HIP POSTITION + ROTATION, multi model prediction. 
# Removing not used element(everthing besides hip) from the dataset
#df = df.drop(df.columns[PREDICITION_SPLIT_JOINTS_VALUE:], axis=1)
#df_target = df_target.drop(df_target.columns[PREDICITION_SPLIT_JOINTS_VALUE:], axis=1)

df = df.drop(df.columns[87:], axis=1)
df_target = df.shift(-PREDICITION_VALUE_IN_FRAMES)

# Removing prediciton value from end of dfs
x_data = df.values[0:-PREDICITION_VALUE_IN_FRAMES]
y_data = df_target.values[:-PREDICITION_VALUE_IN_FRAMES]

print(df.head())
print(df_target.head())


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

num_x_signals = x_data.shape[1]
num_y_signals = y_data.shape[1]



# Scaling the data to be easier handle by the RNN
# Initianig a new scaler-object for x scaling

x_scaler = MinMaxScaler()
x_train_scaled = x_scaler.fit_transform(x_train)
x_test_scaled = x_scaler.transform(x_test)

# Initiating a new scaler-object for y scaling
y_scaler = MinMaxScaler()
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)



# rounding in numps



def batch_generator(batch_size, sequence_length):
    while True:
        # Create new array for batch-X (INPUT)
        x_shape = (batch_size, sequence_length, num_x_signals)
        x_batch = np.zeros(shape=x_shape, dtype=np.float16)

        # Create new array for batch-Y (OUTPUT)
        y_shape = (batch_size, sequence_length, num_y_signals)
        y_batch = np.zeros(shape=y_shape, dtype=np.float16)

        # FILL with new x,y 
        for i in range(batch_size):
            # Get random start index in df
            idx = np.random.randint(num_train - sequence_length)
            
            # Fill with values
            x_batch[i] = x_train_scaled[idx:idx+sequence_length]
            y_batch[i] = y_train_scaled[idx:idx+sequence_length]
        
        # Yield return x,y 
        yield (x_batch, y_batch)


# Create new batch of new data 
generator = batch_generator(batch_size=batch_size, sequence_length=sequence_length)

# Return the new iteration of generator, generator yields the return until asked to provide new data
x_batch, y_batch = next(generator)




# Define validation dataset
validation_data = (np.expand_dims(x_test_scaled, axis=0), np.expand_dims(y_test_scaled, axis=0))


# Building the acutal modal, building sequential keras layout
model = tf.keras.Sequential()


# Defining Layers
model.add(CuDNNLSTM(units=256,return_sequences=True, input_shape=(None, num_x_signals,)))
model.add(Dense(num_y_signals), activation="relu")
model.compile(loss="mean_squared_error", optimizer=optimizer, metrics = ["accuracy"])
model.summary()


# Start training and evaluating

model.fit_generator(generator=generator, epochs=100, steps_per_epoch=1000, validation_data=validation_data, callbacks=callbacks)


try:
    model.load_weights(path_checkpoint)
except Exception as error:
    print("Error trying to load checkpoint.")
    print(error)

result = model.evaluate(x=np.expand_dims(x_test_scaled, axis=0),y=np.expand_dims(y_test_scaled, axis=0))

model.save(prefix)
test_pred = x_test_scaled[0]
test_pred = np.expand_dims(test_pred, axis=0)
print(test_pred)
model_pred = model.predict(np.expand_dims(test_pred, axis=0))
print("Shape prediciton: ", model_pred.shape)
print("Model predicition: ",model_pred )
print("Actual value: ",y_test_scaled[0])



