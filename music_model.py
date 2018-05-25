from keras import Sequential
from keras.layers import TimeDistributed, Convolution1D, MaxPooling1D, Dropout, Flatten, BatchNormalization, LSTM, \
    Bidirectional, Dense


def music_model(frame_size, feature_count, channels):
    model = Sequential()

    model.add(Dense(32, activation='relu', input_dim=24))
    model.add(Dense(32, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.25))

    model.add(Dense(128, activation='relu'))

    model.add((Dropout(0.25)))

    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(16, activation='sigmoid'))


    # # Add x3 Convolutional Layers
    # model.add(Convolution1D(32, 3, activation='relu', input_shape=(frame_size, feature_count)))
    # model.add(Convolution1D(32, 3, activation='relu'))
    # model.add(MaxPooling1D(2, 2))
    #
    # model.add(Dropout(0.25))
    #
    # # Add x3 Convolutional Layers (Total 6)
    # model.add(Convolution1D(64, 3, activation='relu'))
    # model.add(Convolution1D(64, 3, activation='relu'))
    # model.add(MaxPooling1D(2, 2))
    #
    # model.add(Dropout(0.25))
    #
    # # Add x3 Convolutional Layers (Total 9)
    # model.add(Convolution1D(64, 3, activation='relu'))
    # model.add(Convolution1D(64, 3, activation='relu'))
    # model.add(MaxPooling1D(2, 2))
    #
    # model.add(Dropout(0.25))
    #
    # model.add(Flatten())
    # model.add(BatchNormalization())
    #
    # # Add x2 Reccurrent Layers
    # model.add(LSTM(64, return_sequences=True))
    # model.add(LSTM(64, return_sequences=True))
    #
    # model.add(Dropout(0.25))
    # # model.add(Flatten())
    # model.add(Dense(12, activation='sigmoid'))


    # Add x3 Convolutional Layers
    model.add(TimeDistributed(Convolution1D(32, 3, activation='relu'), input_shape=(frame_size, feature_count, channels)))
    model.add(TimeDistributed(Convolution1D(32, 3, activation='relu')))
    model.add(TimeDistributed(MaxPooling1D(2, 2)))

    model.add(Dropout(0.25))

    # Add x3 Convolutional Layers (Total 6)
    model.add(TimeDistributed(Convolution1D(64, 3, activation='relu')))
    model.add(TimeDistributed(Convolution1D(64, 3, activation='relu')))
    model.add(TimeDistributed(MaxPooling1D(2, 2)))

    model.add(Dropout(0.25))

    model.add(TimeDistributed(Flatten()))
    model.add(BatchNormalization())

    # Add x2 Reccurrent Layers
    model.add(Bidirectional(LSTM(128, return_sequences=True)))
    model.add(Bidirectional(LSTM(128, return_sequences=True)))

    model.add(Dropout(0.25))
    #model.add(Flatten())
    model.add(TimeDistributed(Dense(12, activation='sigmoid')))

    return model
