import pickle
import re
import ujson
import collections

import antlr4
from chord_labels import parse_chord, chord_labels
from progressbar import ProgressBar, Bar, Percentage, AdaptiveETA, Counter
from numpy import sum

print("Opening files")
with open('dataset_values.pickle', 'rb') as values:
    #print('opening values')
    formatted_values = pickle.load(values)

with open('dataset_chroma.pickle', 'rb') as chroma:
    #print('opening chroma')
    formatted_chroma = pickle.load(chroma)

print("Files Opened\n")

cleaned_keys = []
cleaned_chroma = []
key_binary_pairs = {}
blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
blank12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]



# How many frames to look at per chord:
frame_size = 20
# Step size per time sample in chroma files
timestep_abs = 0.046439909

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
# [fileid, [time, chord]]

# [intTime, [x24 avg vals]]
# [[x24 vals], chord]


# returns averaged list from formatted_chroma
def average_chroma_by_time(id, start_time, end_time):
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


def get_frames_by_time(id, chord_time):
    blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    timestep = round(timestep_abs, 9)

    values = []
    chord_timestamps = list(formatted_values[id])

    start_time = chord_time - (timestep * 15)
    end_time = chord_time + (timestep * 15)
    end_time_bounded = end_time

    if start_time < 0.0:
        start_num_diff = int(abs(start_time - timestep) / timestep)
        print("NUM BEFORE: %s" % start_num_diff)
        for i in range(start_num_diff):
            values.append(blank)
        start_time = timestep
    if end_time > list(formatted_chroma[id])[-1]:
        end_time_bounded = list(formatted_chroma[id])[-1]

    current_time = start_time

    while current_time < end_time_bounded:
        values.append(formatted_chroma[id][current_time])
        print("Added time: %s" % current_time)
        current_time += timestep
        current_time = round(current_time, 9)

    if end_time > list(formatted_chroma[id])[-1]:
        end_num_diff = int(abs(end_time - list(formatted_chroma[id])[-1]) / timestep)
        print("NUM END: %s" % end_num_diff)
        for i in range(end_num_diff):
            values.append(blank)

    return values

def get_frames_by_time(id, chord_time, num_before, num_after):
    vals = []
    timestamps = list(formatted_chroma[id])
    start_num_to_add = num_before
    end_num_to_add = num_after
    start_to_add_blank = 0
    end_to_add_blank = 0

    for time in range(len(timestamps)):
        # print("Time: %s" % timestamps[time])
        # if time == formatted_values[id][999]:
        #     # print("End: %s" % timestamps[time])
        #     return vals
        if time == chord_time or timestamps[time] < chord_time < timestamps[time+1] or timestamps[time+1] > chord_time:
            # print("In chord time range")
            if len(timestamps[:time]) < start_num_to_add:
                start_to_add_blank = start_num_to_add - len(timestamps[:time])
                start_num_to_add -= start_to_add_blank
            if len(timestamps[time:]) < end_num_to_add:
                end_num_to_add = len(timestamps[time:])-1
                end_to_add_blank = num_after - end_num_to_add

            # print("Start num to add: %s" % start_num_to_add)
            # print("End num to add: %s" % end_num_to_add)
            # print("Start to add: %s" % start_to_add_blank)
            # print("End to add: %s" % end_to_add_blank)

            # Chord time to middle
            vals.append(formatted_chroma[id][timestamps[time]])

            #add to front as decreasing
            i = 1
            while start_num_to_add > 0:
                vals.insert(0, formatted_chroma[id][timestamps[time - i]])
                i += 1
                start_num_to_add -= 1

            #add to back as increasing
            i = 1
            while end_num_to_add > 0:
                try:
                    vals.append(formatted_chroma[id][timestamps[time + i]])
                except IndexError:
                    pass
                i += 1
                end_num_to_add -= 1

            if len(timestamps[:time]) < num_before:
                for i in range(start_to_add_blank):
                    vals.insert(0, blank)

            if len(timestamps[time:]) < num_after:
                for i in range(end_to_add_blank):
                    vals.append(blank)


            return vals

    return vals


# cleaned_data[0] = average_chroma_by_time(3, 148, 149)
# print(str(cleaned_data))



# start_test = get_frames_by_time(3, 7.3469387e-2)
# mid_test = get_frames_by_time(3, 5.015510204)
# end_test = get_frames_by_time(9999, 0.743038548)
# print(start_test)
# print(len(start_test))
# print(mid_test)
# print(len(mid_test))
# print(end_test)
# print(len(end_test))

num_excepted = 0

with open('file_ids.txt', 'r') as idList:
    print("--CLEANING FILES: 890 TODO--\n")
    progress_bar = ProgressBar(widgets=['PROCESSED: ', Counter(), '/890   ', Bar('>'), Percentage(), ' --- ', AdaptiveETA()], maxval=891)
    progress_bar.start()
    for i, id in enumerate(idList):
        progress_bar.update(value=i)
        #id = int(id.strip('\n'))
        #print("CURRENT ID: %s" % id)
        id = 3
        for index, time in enumerate(formatted_values[id]):
            if time == 999:
                break
            num_chords = range(len(formatted_values[id][time]))
            try:
                next_time = list(formatted_values[id])[index + 1]
                #print("NEXT TIME: " + str(next_time))
                if next_time == 999:
                    break
                else:
                    #print("NEXT TIME = 999 (END)")
                    steps_between_chords = len(formatted_chroma[id][time:next_time])
                    time_increment = (next_time-time)/steps_between_chords
                    print("steps between chords: {}".format(steps_between_chords))
                    # print("End time: " + str(end_time))
                    # print("i: " + str(i))
                    if steps_between_chords > 62:
                        try:
                            num_steps = int(steps_between_chords / 31)
                            print("num steps: {}".format(num_steps))
                            blank_timestamps = []
                            for i in range(num_steps):
                                curr_time = (num_steps / steps_between_chords) * (i + 1)
                                print("curr_time: {}".format(curr_time))
                                blank_timestamps.append(get_frames_by_time(id, curr_time, 10, 20))
                                
                        except BaseException:
                            num_excepted += 1

                    for i in num_chords:
                        key = str(formatted_values[id][time][i])

                        if ' ' in key:
                            key = key.split(' ')[0]
                        key = re.sub(r" ?\([^)]+\)", "", key)
                        key = re.sub(r"/[^)]+", "", key)
                        if '*' not in key and key != "" and key != "&pause" and key != '5':
                            try:
                                key_binary = parse_chord(key).tones_binary
                                hold = []
                                for i in range(15):
                                    hold.append(blank12)
                                hold.append(key_binary)
                                for i in range(15):
                                    hold.append(blank12)
                                cleaned_keys.append(hold)
                                cleaned_chroma.append(get_frames_by_time(id, time, 10, 20))
                                key_binary_pairs[tuple(key_binary)] = key
                            except BaseException:
                                num_excepted += 1
                            # print("CLEANED DATA [" + str(formatted_values[id][time][i]) + "]: " + str(cleaned_data[formatted_values[id][time][i]]))
                    break






                # else:
                #     #print("num " + str(len(formatted_values[id][time])))
                #     time_increment = (next_time - time) / (len(formatted_values[id][time]))
                #     for i in num_chords:
                #         end_time = (time + (time_increment * (i + 1)))
                #         key = str(formatted_values[id][time][i])
                #         steps_between_chords = (end_time - time) / time_increment
                #         print("steps between chords: {}".format(steps_between_chords))
                #         # print("End time: " + str(end_time))
                #         # print("i: " + str(i))
                #         if steps_between_chords > 32:
                #             num_steps = int(steps_between_chords / 31)
                #             print("num steps: {}".format(num_steps))
                #             blank_timestamps = []
                #             for i in range(num_steps):
                #                 curr_time = (num_steps/steps_between_chords)*(i+1)
                #                 print("curr_time: {}".format(curr_time))
                #                 blank_timestamps.append(get_frames_by_time(id, curr_time, 10, 20))
                #
                #         if ' ' in key:
                #             key = key.split(' ')[0]
                #         key = re.sub(r" ?\([^)]+\)", "", key)
                #         key = re.sub(r"/[^)]+", "", key)
                #         if '*' not in key and key != "" and key != "&pause" and key != '5':
                #             try:
                #                 key_binary = parse_chord(key).tones_binary
                #                 hold = []
                #                 for i in range(15):
                #                     hold.append(blank12)
                #                 hold.append(key_binary)
                #                 for i in range(15):
                #                     hold.append(blank12)
                #                 cleaned_keys.append(hold)
                #                 cleaned_chroma.append(get_frames_by_time(id, time, 10, 20))
                #                 key_binary_pairs[tuple(key_binary)] = key
                #             except BaseException:
                #                 num_excepted += 1
                #             # print("CLEANED DATA [" + str(formatted_values[id][time][i]) + "]: " + str(cleaned_data[formatted_values[id][time][i]]))
            except IndexError:
                None


print("NUM EXCEPTED DUE TO PARSER: %s" % num_excepted)

def nested_list_count(l):
    return sum(1+nested_list_count(i) for i in l if isinstance(i,list))

for id, list in enumerate(cleaned_chroma):
    if len(cleaned_chroma[id]) != 31:
        print("not 31 : %s" % id)
        raise UserWarning


print('\n')
print("<------------------------------------------------------->")
print("<------------------COUNTING KEYS------------------------>")
print("<------------------------------------------------------->")

# num_keys = collections.Counter(cleaned_keys)
# for key in sorted(num_keys, key=num_keys.get):
#     if num_keys[key] < 1000:
#         while key in cleaned_keys:
#             index = cleaned_keys.index(key)
#             cleaned_keys.remove(key)
#             cleaned_chroma.__delitem__(index)

#print(str(cleaned_keys))
#print(str(cleaned_chroma))
print("NUM OBJECTS: " + str(len(cleaned_keys)))

with open("cleaned_keys.json", 'w') as file:
    ujson.dump(cleaned_keys, file)

with open("cleaned_chroma.json", 'w') as file:
    ujson.dump(cleaned_chroma, file)

with open("key_binary_pairs.json", 'w') as file:
    ujson.dump(key_binary_pairs, file)

print("DONE SAVING")
