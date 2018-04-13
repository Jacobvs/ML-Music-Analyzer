import glob
import regex as re
import pickle
import collections

files = collections.OrderedDict()
folderID = 0000

for folder in glob.glob('annotations/*/'):
    print(folder)
    folderID = folder.split('/')[1]
    folderID = folderID.lstrip('0')
    folderID = int(folderID)
    print(folderID)
    for txtFile in glob.glob(folder + '/*.txt'):
        with open(txtFile) as file:

            values = collections.OrderedDict()

            strFile = str(file.read())
            # try:
            #     strFile = strFile.split('silence')[1]
            # except IndexError:
            #     print("No Silence found")

            strFile = strFile.split('\n')
            print (strFile)
            for line in strFile:

                isTonic = not re.findall('(.*?)# tonic', line, re.S)


                #print(line)
                #add start from 0.0

                if isTonic:
                    foundEnd = re.findall('^(?!0.0	silence)(.*?)	silence', line, re.S)
                    foundChords = re.findall('\\| (.*?) \\|', line, re.S, overlapped=True)
                    foundTimestamp = re.findall('(.*?)	', line, re.S)

                    if not foundEnd:
                        if not foundTimestamp:
                            print("No timestamp found")
                        else:
                            if not foundChords:
                                print("No Chord")
                            else:
                                timestamp = float(foundTimestamp[0])
                                chords = foundChords
                                values[timestamp] = chords
                                print("Timestamp: " + foundTimestamp[0])
                                print("Chords: " + str(foundChords))
                    else:
                        timestamp = float(foundTimestamp[0])
                        values[999] = timestamp
                        print("END: " + line)
                        break

            print("VALUES DICTIONARY: " + str(values))
            files[folderID] = values

print("FILES DICTIONARY: " + str(files))
with open("dataset_values.pickle", 'wb') as handle:
    pickle.dump(files, handle, pickle.HIGHEST_PROTOCOL)


# chromaFiles = collections.OrderedDict()
#
# for folder in glob.glob('metadata/*/'):
#     #print(folder)
#     folderID = folder.split('/')[1]
#     folderID = folderID.lstrip('0')
#     folderID = int(folderID)
#     print("FILE ID: " + str(folderID))
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
#                     timestamp = float(vals[1])
#                     chromaVals = vals[2:]
#                     chromaVals = list(map(float, chromaVals))
#                     values[timestamp] = chromaVals
#
#             chromaFiles[folderID] = values
#
# with open("dataset_chroma.pickle", 'wb') as handle:
#     print("dumping")
#     pickle.dump(chromaFiles, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
# print("DONE")
