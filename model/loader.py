import mfcc
import preprocess
import os
import librosa
import pickle
from matplotlib import pyplot as plt

def load_audio(path):
    """
    Load the audio file using librosa.

    Parameters
    ----------
    path: str
        The audio file path.

    Returns
    -------
    signal: numpy.ndarray
        The loaded audio signal.
    sample_rate: int
        The audio signal sampling rate.
    """

    signal, sample_rate = librosa.load(path, sr=44100, mono=True)
    return signal, sample_rate

def load_all():
    """
    Load all audio file for each class in dataset folder, then preprocess the audio using several method in preprocess module and extract the feature using mfcc module. After that, append the flatten extraction result to the cepstral coefficient list and the label to the label list.

    Returns
    -------
    cepstral_coefficients: numpy.ndarray
        The list of audio in cepstral coefficient form after feature extration using mfcc.
    labels: numpy.ndarray
        The list of labels.
    """
    cepstral_coefficients = []
    labels = []

    PATH = "./dataset/"

    classes = os.listdir(PATH)

    for idx, label in enumerate(classes):
        for i, file in enumerate(os.listdir(os.path.join(PATH, label))):
            signal, sample_rate = load_audio(os.path.join(PATH, label, file))
            audio = preprocess.preprocess(signal, sample_rate)
            cc = mfcc.mfcc(audio, sample_rate, 2048, 25, 40)
            cepstral_coefficients.append(cc.flatten())
            labels.append(idx)

    return cepstral_coefficients, labels

def save_model(model):
    """
    Save the model using pickle library.

    Parameter
    -------
    model: RandomForestClassifier | None
        The model to be saved.
    """
    with open('model.pkl','wb') as f:
        pickle.dump(model,f)

def load_model():
    """
    Load the model file using pickle library.

    Returns
    -------
    model: RandomForestClassifier
        The loaded model.
    """
    global model
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model