import glob
import re
import ujson
import collections

# with open("file_ids.txt", "wb") as file:
#     for folderID in glob.glob("annotations/*/"):
#         folderID = folderID.split('/')[1]
#         folderID = folderID.lstrip('0')
#         file.write(folderID + "\n")


#cleaned_data = collections.OrderedDict()

# def f3(seq):
#    # Not order preserving
#    keys = {}
#    for e in seq:
#        keys[e] = 1
#    return keys.keys()


with open("cleaned_keys.json", "r") as keyfile:
    with open("key_binary_pairs.json", 'r') as keypairfile:
        with open("possible_chords.txt", 'w') as out:
            cleaned_keys = ujson.load(keyfile)
            key_pairs = ujson.load(keypairfile)
            #cleaned_chroma = ujson.load(chromafile)
            #print(collections.Counter(cleaned_keys))
            cleaned_keys = [tuple(x) for x in cleaned_keys]
            keyss = collections.Counter(cleaned_keys)
            for key in sorted(keyss, key=keyss.get):
                abs_key = key_pairs[str(key)]
                out.write(str(abs_key) + ": " + str(key) + ", " + str(keyss[key]) + "\n")
            # num_keys = collections.Counter(cleaned_keys)
            # for key in sorted(num_keys, key=num_keys.get):
            #     out.write(str(key) + ", " + str(cleaned_keys[key]) + "\n")
            #     if num_keys[key] < 50:
            #         for index, key2 in enumerate(cleaned_keys):
            #             if key == key2:
            #                 print("TO BE DELETED KEY: %s" % cleaned_keys[index])
            #                 print("TO BE DELETED CHROMA: %s" % cleaned_chroma[index])