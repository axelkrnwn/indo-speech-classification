import sys
import loader
import preprocess
import mfcc
from scipy.signal import resample
import model
import pandas as pd
import numpy as np

if len(sys.argv) > 1:

    path = sys.argv[1]
    print(path)
    signal, sample_rate = loader.load_audio(path)
    audio = preprocess.preprocess(signal, sample_rate)
    cc = mfcc.mfcc(audio, sample_rate, 2048, 25, 40).flatten()
    resampled = resample(cc, num=3560)

    classes = ['Begal', 'Kebakaran', 'Kecelakaan', 'Maling', 'Pencuri', 'Rampok', 'Tabrakan']
    X = preprocess.normalize(resampled.reshape(1, -1))
    X = preprocess.reduce_dimension(X)
    loaded_model = model.Model()
    res = loaded_model.test(X)
    idx = np.argmax(res)

    if np.abs(res[0][idx] - 0.5) < 0.1:
        print("Unrecognized")
    else:
        print(classes[np.argmax(res[0])])
print('No audio')