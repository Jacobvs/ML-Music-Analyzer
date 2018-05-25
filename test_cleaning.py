import json
import pickle
import numpy as np
import ujson

print("Opening Files")

with open("cleaned_x.json", 'r') as file:
    cleaned_chroma = ujson.load(file)

with open("cleaned_y.json", 'r') as file:
    cleaned_chords = ujson.load(file)

#with open("key_binary_pairs.json", 'r') as file:
    #key_binary_pairs = ujson.load(file)

print("Files Opened")


hold_x = []
hold_y = []

print(len(cleaned_chroma))

with open("file_ids_subset.txt", 'r') as idFile:
    for id in idFile:
        id = int(id.strip('\n'))
        for thing1 in cleaned_chroma[str(id)]:
            hold_x.append(thing1)
        for thing2 in cleaned_chords[str(id)]:
            hold_y.append(thing2)

# samples x 100 x 24
print(hold_x[666][99][23])

cleaned_x = np.array(hold_x)
cleaned_y = np.array(hold_y)

# format in [file id][chroma (0) or chord (1)][slice num to look at (per 100)][index within slice]
print(cleaned_x.shape)
print(cleaned_y.shape)

# final_X = []
# final_Y = []
#
# with open("file_ids_subset.txt", 'r') as idFile:
#     for id in idFile:
#         id = int(id.strip('\n'))
#         final_X.append(cleaned_chroma[str(id)])
#         final_Y.append(cleaned_chords[str(id)])
#
#
# final_X = np.array(final_X)
# final_Y = np.array(final_Y)
# final_X = np.expand_dims(final_X, axis=3)
#
# print("x shape: {} -- y shape: {}".format(final_X.shape, final_Y.shape))




