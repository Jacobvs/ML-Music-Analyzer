import glob

with open("file_ids.txt", "wb") as file:
    for folderID in glob.glob("annotations/*/"):
        folderID = folderID.split('/')[1]
        folderID = folderID.lstrip('0')
        file.write(folderID + "\n")