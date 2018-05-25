import numpy as np
import ujson
from matplotlib import pyplot as plt
from keras.models import load_model
from progressbar import ProgressBar, Counter, Percentage, Bar, AdaptiveETA
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import hamming_loss
from sklearn.metrics import roc_auc_score
from music21 import chord

print(chord.Chord([0,4,7]).pitchedCommonName)

print("Opening files")
with open('cleaned_x.json', 'r') as xfile:
    cleaned_X = np.array(ujson.load(xfile))

with open('cleaned_y.json', 'r') as yfile:
    cleaned_Y = np.array(ujson.load(yfile))

with open('key_binary_pairs.json', 'r') as pairfile:
    key_binary_pairs = ujson.load(pairfile)

print("Files Opened\n")
print("Num objects: %s" % len(cleaned_X))


np.random.seed(8)
np.set_printoptions(threshold=np.nan)


cleaned_X = np.expand_dims(cleaned_X, axis=3)

print("x shape: {} -- y shape: {}".format(cleaned_X.shape, cleaned_Y.shape))


# Create train, val, test split
train_X, temp_X, train_Y, temp_Y = train_test_split(cleaned_X, cleaned_Y, test_size=.3)
del cleaned_X
del cleaned_Y
validation_X, test_X, validation_Y, test_Y = train_test_split(temp_X, temp_Y, test_size=.4)
del temp_X
del temp_Y

print("KEY SHAPE: %s" % str(train_Y.shape))
print("CHROMA SHAPE: %s" % str(train_X.shape))

model = load_model("trained_music_model.hdf5")

# Y_proba = model.predict(test_X[2], batch_size=32, verbose=1).reshape(-1, 100)
# Y_classes = (Y_proba >= 0.5).astype(np.int32)
#
# predictions = model.predict(np.expand_dims(test_X[2], axis=0), batch_size=32)
# ground_truth = test_Y[2]
#
# label_predictions = []
# for arr in predictions:
#     for arr2 in arr:
#         blank_arr = [int(round(x)) for x in arr2]
#         label_predictions.append(key_binary_pairs[str(tuple(blank_arr))])
#
# label_truth = []
# for arr in ground_truth:
#     for arr2 in arr:
#         blank_arr = [int(round(x)) for x in arr2]
#         label_predictions.append(key_binary_pairs[str(tuple(blank_arr))])
#
#
# print(label_predictions)
# print(ground_truth)


predicted_probability = model.predict(validation_X, batch_size=32, verbose=1)
predicted_probability_flat = predicted_probability.reshape(-1, 100)
predicted_classes = (predicted_probability >= 0.5).astype(np.int32)
predicted_classes_flat = (predicted_probability_flat >= 0.5).astype(np.int32)

print(predicted_probability_flat.shape)

print('Validation Data Accuracy:')
print('accuracy:', accuracy_score(validation_Y.reshape(-1, 100), predicted_classes_flat))
print('hamming score:', 1 - hamming_loss(validation_Y.reshape(-1, 100), predicted_classes_flat))
print('AUC:', roc_auc_score(validation_Y.reshape(-1, 100).flatten(), predicted_probability_flat.flatten()))


print('Plotting Chord Error')

print(len(validation_Y.reshape(-1, 12)))

start_num = 0
length = 2000
#len(Y_valid.reshape(-1, 12))

sliced = slice(start_num, start_num + length)
true_labels = validation_Y.reshape(-1, 12)[sliced].T
predicted_probability_flat = predicted_probability_flat.reshape(-1, 12)[sliced].T
predicted_classes_flat = predicted_classes_flat.reshape(-1, 12)[sliced].T

plot, (subplot1, subplot2, subplot3) = plt.subplots(3, 1)
#plot.suptitle('Music Model Test')
plot.set_size_inches((13, 10))

subplot1.imshow(predicted_probability_flat, vmin=0, vmax=1)
subplot1.set_aspect('auto')
subplot1.set_ylabel('Pitch Class')
subplot1.set_title('Predicted Chords')

subplot2.imshow(true_labels, vmin=0, vmax=1)
subplot2.set_aspect('auto')
subplot2.set_ylabel('Pitch Class')
subplot2.set_title('True Chords')

subplot3.imshow(predicted_classes_flat - true_labels, vmin=-1, vmax=1)
subplot3.set_aspect('auto')
subplot3.set_ylabel('Pitch Class')
subplot3.set_title('Error in Predictions')

error_analysis_file = 'chord_error_analysis.png'
print(error_analysis_file)
plt.savefig(error_analysis_file)


chords = []
excepted = []
blank = []

for arr in predicted_classes:
    for i, binary_arr in enumerate(arr):
        pitch_class = [i for i in range(len(binary_arr)) if binary_arr[i] == 1]
        if pitch_class != blank:
            print(pitch_class)
            c = chord.Chord(pitch_class)
            chords.append(c)
        else:
            excepted.append(i)





