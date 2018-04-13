#make one dict containing only
#[[24 AVERAGED CHROMA VALS FOR +/- SECOND CHORD IS NOTED AT], CHORD]

#import pickle files
import pickle
import ujson
import collections
import warnings

from numpy import sum

with open('dataset_values.pickle', 'rb') as values:
    print('opening values')
    formatted_values = pickle.load(values)

with open('dataset_chroma.pickle', 'rb') as chroma:
    print('opening chroma')
    formatted_chroma = pickle.load(chroma)

cleaned_data = collections.OrderedDict()

# id = 3
#
# lastTime = int(list(reversed(formatted_values[id].keys()))[1])
# print("LAST: " + str(lastTime))
#
# for time in reversed(formatted_values[id]):
#     intTime = int(time)
#     print(str(intTime))
#
#     #for chromaTime in reversed(formatted_chroma[id]):



# [fileID, [time, [x24 vals]]]
#[fileid, [time, chord]]

# [intTime, [x24 avg vals]]
# [[x24 vals], chord]


# returns averaged list from formatted_chroma
def average_chroma_by_time(id, start_time, end_time):
    blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    averaged_vals = blank
    added = blank

    for time in list(formatted_chroma[id]):
        if time > end_time:
            # print("ADDED: " + str(added))
            for num, val in enumerate(added):
                if val != 0:
                    # print("num added: " + str(added[num]))
                    averaged_vals[num] = averaged_vals[num] / added[num]

            # print(str(averaged_vals))
            break

        if end_time >= time >= start_time:
            averaged_vals = list(sum([averaged_vals, formatted_chroma[id][time]], axis=0))
            for num, val in enumerate(formatted_chroma[id][time]):
                if val != 0:
                    added[num] += 1
                    # print("INDEX: " + str(num))
            # print("EQUALS: " + str(averaged_vals))
            # print("EQUALS SIZE: " + str(cleaned_vals[intTime]))

    return averaged_vals


#cleaned_data[0] = average_chroma_by_time(3, 148, 149)
#print(str(cleaned_data))


with open('file_ids.txt', 'r') as idList:
    for id in idList:
        id = int(id.strip('\n'))
        warnings.warn("ID ")
        for index, time in enumerate(formatted_values[id]):
            if time == 999:
                break
            num_chords = range(len(formatted_values[id][time]))
            try:
                next_time = list(formatted_values[id])[index+1]
                print("NEXT TIME: " + str(next_time))
                if next_time == 999:
                    print("NEXT TIME = 999")
                    time_increment = (float(formatted_values[id][999]) - time) / len(formatted_values[id][time])
                    for i in num_chords:
                        end_time = (time + (time_increment * (i + 1)))
                        print("End time: " + str(end_time))
                        print("i: " + str(i))
                        cleaned_data[formatted_values[id][time][i]] = average_chroma_by_time(id, time, end_time)
                        print("CLEANED DATA [" + str(formatted_values[id][time][i]) + "]: " + str(
                            cleaned_data[formatted_values[id][time][i]]))
                    break
                else:
                    print("num " + str(len(formatted_values[id][time])))
                    time_increment = (next_time-time) / (len(formatted_values[id][time]))
                    for i in num_chords:
                        end_time = (time+(time_increment*(i+1)))
                        print("End time: " + str(end_time))
                        print("i: " + str(i))
                        cleaned_data[formatted_values[id][time][i]] = average_chroma_by_time(id, time, end_time)
                        print("CLEANED DATA [" + str(formatted_values[id][time][i]) + "]: " + str(cleaned_data[formatted_values[id][time][i]]))
            except IndexError:
                warnings.warn("INDEX ERROR: " + str(index))


print(str(cleaned_data))
print("NUM OBJECTS: " + str(len(cleaned_data.keys())))

with open("cleaned_data.json", 'w') as file:
    ujson.dump(cleaned_data, file)

with open("possible_chords.txt", 'w') as file:
    for index, key in enumerate(cleaned_data.keys()):
        if key not in list(cleaned_data.keys())[index:]:
            file.write(str(key) + "\n")

