import ast
import json
import pickle
import ujson
import collections
import numpy as np

from chord_labels import parse_chord
from progressbar import ProgressBar, Bar, Percentage, AdaptiveETA, Counter

print("Opening files")
with open('dataset_chords.json', 'r') as values:
    formatted_chords = ujson.load(values)

with open('dataset_chroma.pickle', 'rb') as chroma:
    formatted_chroma = pickle.load(chroma)

print("Files Opened\n")

blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
blank12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

values = collections.OrderedDict()
cleaned_chroma = []
cleaned_chords = []
final_chroma = {}
final_chords = {}
key_binary_pairs = {}


def slice_vals(chroma_vals, chord_vals, slice_size):
    num_slices = int(len(chroma_vals)/slice_size)
    sliced_chroma = []
    sliced_chords = []
    for i in range(num_slices):
        sliced_chroma.append(chroma_vals[i*slice_size:(i+1)*100])
        sliced_chords.append(chord_vals[i*100:(i+1)*100])

    remaining_chroma = chroma_vals[num_slices*100:]
    remaining_chords = chord_vals[num_slices*100:]

    for i in range(100-len(remaining_chroma)):
        remaining_chroma.append(blank)
        remaining_chords.append(blank12)

    if len(remaining_chroma) > 0:
        sliced_chroma.append(remaining_chroma)
        sliced_chords.append(remaining_chords)

    del remaining_chords
    del remaining_chroma

    return sliced_chroma, sliced_chords



with open('file_ids.txt', 'r') as idList:
    print("--CLEANING FILES: 890 TODO--\n")
    progress_bar = ProgressBar(widgets=['PROCESSED: ', Counter(), '/890   ', Bar('>'), Percentage(), ' --- ', AdaptiveETA()], maxval=891)
    progress_bar.start()
    for i, id in enumerate(idList):
        progress_bar.update(value=i)
        id = int(id.strip('\n'))

        chord_iter = iter(formatted_chords[str(id)].keys())
        curr_chord = next(chord_iter)
        curr_chord_tuple = ast.literal_eval(curr_chord)
        in_chord = False
        cleaned_chroma = []
        cleaned_chords = []

        chord_nums = 0

        for i, time in enumerate(formatted_chroma[id].keys()):
            if curr_chord_tuple[0] <= time <= curr_chord_tuple[1] and formatted_chords[str(id)][curr_chord] != 'X':
                curr_chord_binary = parse_chord(formatted_chords[str(id)][curr_chord]).tones_binary
                print(curr_chord_binary)
                cleaned_chords.append(curr_chord_binary)
                cleaned_chroma.append(formatted_chroma[id][time])
                key_binary_pairs[tuple(curr_chord_binary)] = formatted_chords[str(id)][curr_chord]
                chord_nums += 1
                in_chord = True
            elif in_chord:
                try:
                    in_chord = False
                    cleaned_chords.append(blank12)
                    cleaned_chroma.append(formatted_chroma[id][time])
                    curr_chord = next(chord_iter)
                    curr_chord_tuple = ast.literal_eval(curr_chord)
                except StopIteration:
                    pass
            else:
                cleaned_chords.append(blank12)
                cleaned_chroma.append(formatted_chroma[id][time])
                if time > curr_chord_tuple[1]:
                    try:
                        in_chord = False
                        cleaned_chords.append(blank12)
                        cleaned_chroma.append(formatted_chroma[id][time])
                        curr_chord = next(chord_iter)
                        curr_chord_tuple = ast.literal_eval(curr_chord)
                    except StopIteration:
                        pass

        sliced = slice_vals(cleaned_chroma, cleaned_chords, 100)
        final_chroma[int(id)] = sliced[0]
        final_chords[int(id)] = sliced[1]
        del sliced

key_binary_pairs[tuple(blank12)] = 'None'



print('\n')
print("<------------------------------------------------------->")
print("<------------------COUNTING KEYS------------------------>")
print("<------------------------------------------------------->")

hold_x = []
hold_y = []

print(len(final_chroma[12]))

with open("file_ids_subset.txt", 'r') as idFile:
    for id in idFile:
        id = int(id.strip('\n'))
        for thing1 in final_chroma[id]:
            hold_x.append(thing1)
        for thing2 in final_chords[id]:
            hold_y.append(thing2)

# samples x 100 x 24
print(hold_x[0][99][23])

cleaned_x = np.array(hold_x)
cleaned_y = np.array(hold_y)

# format in [file id][chroma (0) or chord (1)][slice num to look at (per 100)][index within slice]
print(cleaned_x.shape)
print(cleaned_y.shape)

print("NUM OBJECTS: " + str(len(final_chords)))

# with open("cleaned_chroma.pickle", 'wb') as file:
#     dill.dump(cleaned_chroma, file, protocol=pickle.HIGHEST_PROTOCOL)
#     del cleaned_chroma
#
# with open("cleaned_chords.pickle", 'wb') as file:
#     dill.dump(cleaned_chords, file, protocol=pickle.HIGHEST_PROTOCOL)
#     del cleaned_chords

print("saving chroma")

with open("cleaned_x.json", 'w') as file:
    ujson.dump(hold_x, file)

print("saving chords")

with open("cleaned_y.json", 'w') as file:
    ujson.dump(hold_y, file)

print("saving pairs")

with open("key_binary_pairs.json", 'w') as file:
    ujson.dump(key_binary_pairs, file)

print("DONE SAVING")
