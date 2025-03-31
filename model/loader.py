import mfcc
import preprocess
import os
import librosa
import pickle
from matplotlib import pyplot as plt

def load_audio(path):
    signal, sample_rate = librosa.load(path, sr=44100, mono=True)
    return signal, sample_rate

def load_all():
    cepstral_coefficients = []
    labels = []

    PATH = "./dataset/"

    classes = os.listdir(PATH)

    for idx, label in enumerate(classes):
        for i, file in enumerate(os.listdir(os.path.join(PATH, label))):
            signal, sample_rate = load_audio(os.path.join(PATH, label, file))
            # plt.plot(signal)
            # plt.show()
            audio = preprocess.preprocess(signal, sample_rate)
            # plt.plot(audio)
            # plt.show()
            # break
            cc = mfcc.mfcc(audio, sample_rate, 2048, 25, 40)
            cepstral_coefficients.append(cc.flatten())
            labels.append(idx)

    return cepstral_coefficients, labels

def save_model(model):
    with open('model.pkl','wb') as f:
        pickle.dump(model,f)

def load_model():
    global model
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model