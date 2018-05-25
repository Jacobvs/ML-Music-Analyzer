import ujson
import os
import numpy as np
import pandas as pd
from keras.utils import plot_model
from matplotlib import pyplot as plt
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras.callbacks import ModelCheckpoint, ProgbarLogger, EarlyStopping
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

from music_model import music_model


np.random.seed(8)
np.set_printoptions(threshold=np.nan)

with open("cleaned_keys.json", "r") as keyfile:
    cleaned_keys = ujson.load(keyfile)

with open("cleaned_chroma.json", 'r') as chromafile:
    cleaned_chroma = ujson.load(chromafile)


print("num objects: %s" % len(cleaned_keys))


cleaned_keys = np.array(cleaned_keys)
cleaned_chroma = np.array(cleaned_chroma)
cleaned_chroma = np.expand_dims(cleaned_chroma, axis=3)


# print("KEY SHAPE: %s" % str(one_hot_keys.shape))
# print("CHROMA SHAPE: %s" % str(cleaned_chroma.shape))

# Create train, val, test split
train_X, temp_X, train_Y, temp_Y = train_test_split(cleaned_chroma, cleaned_keys, test_size=.3)
validation_X, test_X, validation_Y, test_Y = train_test_split(temp_X, temp_Y, test_size=.4)
del temp_X
del temp_Y

print("KEY SHAPE: %s" % str(train_Y.shape))
print("CHROMA SHAPE: %s" % str(train_X.shape))

num_epochs = 5
batch_size = 32
frame_size = 31
feature_count = 24



filepath = "model_epoch-{epoch:02d}_val_loss-{val_loss:.4f}_val_acc-{val_acc:.4f}.hdf5"

checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False,
                             mode='max')
progbar = ProgbarLogger(count_mode='samples', stateful_metrics=None)
earlystop = EarlyStopping(monitor='val_loss', min_delta=0.01)


model = music_model(frame_size, feature_count, 1)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(x=train_X, y=train_Y, batch_size=batch_size, epochs=num_epochs, verbose=1,
                    callbacks=[checkpoint, progbar, earlystop], validation_data=(validation_X, validation_Y))



model.save("trained_music_model.hdf5")

plot_model(model, to_file='model.png', show_shapes=True)

print(model.evaluate(test_X, test_Y))
print("PREDICTIONS: %s VS GROUND TRUTH: %s" % (model.predict(np.expand_dims(test_X[10], axis=0), batch_size=batch_size), test_Y[10]))

os.system('afplay /System/Library/Sounds/Ping.aiff')
os.system('afplay /System/Library/Sounds/Ping.aiff')

plt.figure(1)

# summarize history for accuracy
plt.subplot(211)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')

# summarize history for loss
plt.subplot(212)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
