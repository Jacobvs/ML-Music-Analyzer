import glob

import collections
import htk_io.base as base
import htk_io.alignment as alio
import ujson

files = collections.OrderedDict()


for folder in glob.glob('annotations_v2/*/'):
    folderID = folder.split('/')[1]
    folderID = folderID.lstrip('0')
    folderID = int(folderID)
    print("FILE ID: " + str(folderID))
    with open(folder + '/majmin.lab', 'r') as file:

        values = collections.OrderedDict()

        strFile = str(file.read())
        strFile = strFile.split('\n')

        for line in strFile:
            hold = line.split('	')
            print(hold)
            if len(hold) > 2 and hold[2] != 'N':
                values[(float(hold[0]), float(hold[1]))] = hold[2]
                #print(values)

        files[int(folderID)] = values

print(files)

with open("dataset_chords.json", 'w') as file:
    ujson.dump(files, file)



