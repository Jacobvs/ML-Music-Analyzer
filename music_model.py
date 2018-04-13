import glob
import pickle

import collections
import cv2

# with open('dataset_values.pickle', 'rb') as handle:
#     formatted_data = pickle.load(handle)
#
# with open('file_ids.txt') as idList:
#     for fileID in idList:
#         file = open()


with open('dataset_values.pickle', 'rb') as values:
    print('opening values')
    formatted_values = pickle.load(values)

with open('dataset_chroma.pickle', 'rb') as chroma:
    print('opening chroma')
    formatted_chroma = pickle.load(chroma)

#formatted_chroma = collections.OrderedDict()
#
# for folder in glob.glob('metadata/*/'):
#     #print(folder)
#     folderID = folder.split('/')[1]
#     folderID = folderID.lstrip('0')
#     print("FILE ID: " + folderID)
#     for file in glob.glob(folder + '/bothchroma.csv'):
#         with open(file) as chromaFile:
#
#             values = collections.OrderedDict()
#
#             strChromaFile = str(chromaFile.read())
#             # try:
#             #     strFile = strFile.split('silence')[1]
#             # except IndexError:
#             #     print("No Silence found")
#
#             strChromaFile = strChromaFile.split('\n')
#             #print (strChromaFile)
#             for line in strChromaFile:
#                 if line != '':
#                     vals = line.split(',')
#                     timestamp = vals[1]
#                     chromaVals = vals[2:]
#                     values[timestamp] = chromaVals
#
#             formatted_chroma[folderID] = values

folderID = 3

print(formatted_values[folderID])
print(formatted_chroma[folderID])
