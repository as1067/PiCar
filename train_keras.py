import cv2
from keras import Model,Sequential
import keras.layers as l
import csv
import numpy as np
vidcap = cv2.VideoCapture("epochs/out-video_1.avi")
from keras.optimizers import Adam

# Data preprocessing
print("preparing data")
success = True
images = []
while success:
    success, image = vidcap.read()
    if success:
        # print(image)
        image = np.true_divide(image,255)
        images.append(image)
images = np.asarray(images)
steering = []
with open("epochs/out-key_1.csv") as steer:
    reader = csv.reader(steer,delimiter=",")
    count = 0
    for row in reader:
        if not count == 0:
            steering.append(int(row[2]))
        count+=1
steering = np.asarray(steering)

#Neural Network Setup
batch_size = 5
dropout = .4
model = Sequential()
model.add(l.Conv2D(1024,activation="relu",kernel_size=(5,5),input_shape=(240,320,3),data_format="channels_last"))
model.add(l.Conv2D(512,activation="relu",kernel_size=(5,5),data_format="channels_last"))
model.add(l.Conv2D(256,activation="relu",kernel_size=(5,5),data_format="channels_last"))
model.add(l.Conv2D(128,activation="relu",kernel_size=(3,3),data_format="channels_last"))
model.add(l.Conv2D(64,activation="relu",kernel_size=(3,3),data_format="channels_last"))
model.add(l.Flatten())
model.add(l.Dense(1000,activation="relu"))
model.add(l.Dropout(dropout))
model.add(l.BatchNormalization())
model.add(l.Dense(100,activation="relu"))
model.add(l.Dropout(dropout))
model.add(l.BatchNormalization())
model.add(l.Dense(1,activation="relu"))
model.compile(optimizer=Adam(),loss="mean_squared_logarithmic_error")

#Neural Network Training
print("starting training")
model.fit(images,steering,batch_size=batch_size,epochs=10000)
model.save("checkpoint/model_0.h5")


