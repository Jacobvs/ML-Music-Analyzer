import os
import time
import librosa
import vampyhost
import numpy as np
import collections
import vamp.frames
import scipy.signal
import youtube_dl
import pygame, pygame.sndarray
from vampyhost import load_plugin
from keras.models import load_model
#from matplotlib import pyplot as plt
from music21 import chord
from pygame.time import delay
from vamp.collect import get_feature_step_time, fill_timestamps



############# SONG INPUT ##############
song_name = "aint no rest for the wicked instrumental"
song_type = ".mp3"
use_youtube = True
youtube_url = "https://www.youtube.com/watch?v=9l5L34VqzlU"
#######################################


if use_youtube:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(etx)s',
        'quiet': False
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print(youtube_url)
        info = ydl.extract_info(youtube_url, download=True)
        song_name = info.get('title', None)
        song_type = '.mp3'
        os.rename(song_name+song_type, 'testing/'+song_name+song_type)


def deduce_shape(output_desc):
    if output_desc["hasDuration"]:
        return "list"
    if output_desc["sampleType"] == vampyhost.VARIABLE_SAMPLE_RATE:
        return "list"
    if not output_desc["hasFixedBinCount"]:
        return "list"
    if output_desc["binCount"] == 0:
        return "list"
    if output_desc["binCount"] == 1:
        return "vector"
    return "matrix"


def reshape(results, sample_rate, step_size, output_desc, shape):
    output = output_desc["identifier"]
    out_step = get_feature_step_time(sample_rate, step_size, output_desc)

    if shape == "vector":
        rv = ( out_step,
               np.array([r[output]["values"][0] for r in results], np.float32) )
    elif shape == "matrix":
        outseq = [r[output]["values"] for r in results]
        rv = ( out_step, np.array(outseq, np.float32) )
    else:
        rv = list(fill_timestamps(results, sample_rate, step_size, output_desc))

    return rv


def slice_vals(chroma_vals, slice_size):
    blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    num_slices = int(len(chroma_vals)/slice_size)
    sliced_chroma = []
    for i in range(num_slices):
        sliced_chroma.append(chroma_vals[i*slice_size:(i+1)*100])

    remaining_chroma = list(chroma_vals[num_slices*100:])

    for i in range(100-len(remaining_chroma)):
        remaining_chroma.append(blank)

    if len(remaining_chroma) > 0:
        sliced_chroma.append(remaining_chroma)

    del remaining_chroma

    return sliced_chroma


print("Loading song: {}{}".format(song_name,song_type))

np.set_printoptions(threshold=np.nan)
data, rate = librosa.load("testing/" + song_name + song_type)

print("--LOADED SONG--")

nnls_chroma = load_plugin("nnls-chroma:nnls-chroma", rate, 0x03)
nnls_chroma.set_parameter_value("rollon", 1)

stepsize = nnls_chroma.get_preferred_step_size()
blocksize = nnls_chroma.get_preferred_block_size()
channels = 1
if data.ndim > 1:
    channels = data.shape[0]

nnls_chroma.initialise(channels, stepsize, blocksize)
frames = vamp.frames.frames_from_array(data, stepsize, blocksize)
results = vamp.process.process_with_initialised_plugin(frames, rate, stepsize, nnls_chroma, [nnls_chroma.get_output(5)["identifier"]])
shape = deduce_shape(nnls_chroma.get_output(5))
rv = reshape(results, rate, stepsize, nnls_chroma.get_output(5), shape)

nnls_chroma.unload()
chroma = {shape : rv}


stepsize, chroma_data = chroma['matrix']

structured_chroma = collections.OrderedDict()
timestamp = 0.0
stepsize = stepsize.to_float()
# chroma_data = chroma_data.tolist()

print("Stepsize = {}".format(timestamp+stepsize))
print("Length of song: {}".format(len(chroma_data)))


for index, data in enumerate(chroma_data):
    timestamp = (timestamp + stepsize)
    structured_chroma[timestamp] = chroma_data[index]

sliced_chroma = np.expand_dims(slice_vals(chroma_data, 100), axis=3)
print("Shape: {}".format(sliced_chroma.shape))

model = load_model("trained_music_model.hdf5")

predicted_probability = model.predict(sliced_chroma, batch_size=32, verbose=1)
predicted_probability = predicted_probability.reshape(-1, 100)
predicted_classes = (predicted_probability >= 0.5).astype(np.int32)

predicted_probability_arr = predicted_probability.reshape(-1, 12)
predicted_classes_arr = predicted_classes.reshape(-1, 12)



# plot, (subplot1, subplot2) = plt.subplots(2, 1)
# # plot.suptitle('Music Model Test')
# plot.set_size_inches((6, 10))
#
# subplot1.imshow(predicted_classes_arr, vmin=0, vmax=1)
# subplot1.set_aspect('auto')
# subplot1.set_ylabel('Pitch Class')
# subplot1.set_title('Predicted Chords')
#
# subplot2.imshow(predicted_probability_arr, vmin=0, vmax=1)
# subplot2.set_aspect('auto')
# subplot2.set_ylabel('Pitch Class')
# subplot2.set_title('Predicted Chords (Probability)')
#
#plt.show()


timestamps = list(structured_chroma.keys())
predicted_frequencies = collections.OrderedDict()
predicted_chords = []

with open("testing/predictions/Predicted Chords -- {}.txt".format(song_name), "w") as file:
    #progress_bar = ProgressBar(widgets=['PROCESSED: ', collections.Counter(), '/{}   '.format(len(predicted_classes)), Bar('>'), Percentage(),' --- ', AdaptiveETA()], maxval=len(predicted_classes) + 1)
    #progress_bar.start()
    for i, arr in enumerate(predicted_classes_arr):
        pitch_class = [i for i in range(len(arr)) if arr[i] == 1]
        try:
            if pitch_class:
                c = chord.Chord(pitch_class)
                predicted_frequencies[timestamps[i]] = list([x.frequency for x in c.pitches])
                predicted_chords.append(c.pitchedCommonName)
                file.write("{}  {}  {}\n".format(timestamps[i], pitch_class, c.pitchedCommonName))
            else:
                predicted_frequencies[timestamps[i]] = [0.0]
                predicted_chords.append("No_Chord")
                file.write("{}  {}  No_Chord\n".format(timestamps[i], [0,0,0]))
        except IndexError:
            pass


print("Done Writing Predictions")


print("PLAYING PREDICTED AUDIO:")

def play_for(sample_wave, ms):
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)
    pygame.time.delay(ms)
    sound.stop()

sample_rate = 44100

def sine_wave(hz, peak, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
       Defaults to one second.
    """
    length = sample_rate / float(hz)
    omega = np.pi * 2 / length
    xvalues = np.arange(int(length)) * omega
    onecycle = peak * np.sin(xvalues)
    return np.resize(onecycle, (n_samples,)).astype(np.int16)


last_frequency = []
last_changed_index = -1
time_distributed_sounds = []
time_distributed_chords = []

for i, frequencies in enumerate(predicted_frequencies.values()):
    if frequencies == last_frequency:
        #print("i: {}, last changed index: {}, len: {}".format(i, last_changed_index, len(time_distributed_sounds)))
        time_distributed_sounds[last_changed_index] = (time_distributed_sounds[last_changed_index][0]+stepsize, frequencies)
    else:
        time_distributed_sounds.append((stepsize, frequencies))
        time_distributed_chords.append(predicted_chords[i])
        last_changed_index += 1
    last_frequency = frequencies

#print(time_distributed_sounds)

start_time = time.time()
pygame.mixer.pre_init(sample_rate, -16, 1)
pygame.init()
time_running = 0

for i, sound_tuple in enumerate(time_distributed_sounds):
    time_running += sound_tuple[0]
    print("Time: {} -- Chord: {}".format(time_running, time_distributed_chords[i]))
    if sound_tuple[1] != [0.0]:
        play_for(sum([sine_wave(x, 2048) for x in sound_tuple[1]]), int(sound_tuple[0] * 1000))
    else:
        delay(int(sound_tuple[0] * 1000))


# for timestamp, frequencies in predicted_frequencies.items():
#     while start_time + timestamp > time.time():
#         pass
#
#     if frequencies != [0.0]:
#         print(frequencies)
#         print(sum([sine_wave(x, 4096) for x in frequencies]))
#         play_for(sum([sine_wave(x, 4096) for x in frequencies]), int(stepsize*1000))
#         # play pitch class through speakers
#     print("Time: {} -- Chord: {}".format(timestamp, frequencies))
