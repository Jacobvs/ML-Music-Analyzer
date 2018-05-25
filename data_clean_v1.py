import glob
import collections

for folder in glob.glob('metadata/*/'):
    #print(folder)
    folderID = folder.split('/')[1]
    folderID = folderID.lstrip('0')
    folderID = int(folderID)
    print("FILE ID: " + str(folderID))
    for file in glob.glob(folder + '/bothchroma.csv'):
        with open(file) as chromaFile:

            values = collections.OrderedDict()

            strChromaFile = str(chromaFile.read())
            # try:
            #     strFile = strFile.split('silence')[1]
            # except IndexError:
            #     print("No Silence found")

            strChromaFile = strChromaFile.split('\n')
            #print (strChromaFile)
            for line in strChromaFile:
                if line != '':
                    vals = line.split(',')
                    timestamp = float(vals[1])
                    chromaVals = vals[2:]
                    chromaVals = list(map(float, chromaVals))
                    values[timestamp] = chromaVals

            chromaFiles[folderID] = values