import pickle
import numpy as np
from matplotlib import pyplot as plt

with open('dataset_chroma.pickle', 'rb') as chroma:
    formatted_chroma = pickle.load(chroma)

print(type(formatted_chroma))

chroma = []
for time in formatted_chroma[3]:
    chroma.append(formatted_chroma[3][time])

print(len(chroma))
print(type(chroma))
print(chroma[0])

chroma = np.array(chroma).T
# print(chroma.shape)

def valid_imshow_data(data):
    data = np.asarray(data)
    if data.ndim == 2:
        return True
    elif data.ndim == 3:
        if 3 <= data.shape[2] <= 4:
            return True
        else:
            print('The "data" has 3 dimensions but the last dimension '
                  'must have a length of 3 (RGB) or 4 (RGBA), not "{}".'
                  ''.format(data.shape[2]))
            return False
    else:
        print('To visualize an image the data must be 2 dimensional or '
              '3 dimensional, not "{}".'
              ''.format(data.ndim))
        return False

valid_imshow_data(chroma)

plot, (subplot1) = plt.subplots(1, 1)
plot.suptitle('Chromagram')
plot.set_size_inches((22, 4))

subplot1.imshow(chroma, vmin=0, vmax=1)
subplot1.set_aspect('auto')

chromagram_file = 'sample_chromagram.png'
print(chromagram_file)
plt.savefig(chromagram_file)