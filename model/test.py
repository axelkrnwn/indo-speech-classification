import noisereduce as nr
import numpy as np
from matplotlib import pyplot as plt
from scipy import fftpack as fft
from scipy.io import wavfile
from scipy.signal import get_window, resample, butter, lfilter
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd
import librosa



def framing(audio, sample_rate, hop_size, fft_size):
    
    audio = np.pad(audio, int(fft_size / 2), mode='reflect')
    
    frame_len = np.round(sample_rate * (hop_size / 1000)).astype(int)
    frame_num = int((len(audio) - fft_size) / frame_len)
    audio_frame = np.zeros((frame_num, fft_size))

    for i in range(frame_num):
        audio_frame[i] = audio[i * frame_len: i * frame_len + fft_size]
    
    return audio_frame


def fast_fourier_transform(audio_window_T, fft_size):
    fft_res = np.empty(((fft_size // 2) + 1, audio_window_T.shape[1]), dtype=np.complex64, order='F')

    for i in range(fft_res.shape[1]):
        fft_res[:, i] = fft.fft(audio_window_T[:, i],axis=0)[:fft_res.shape[0]]

    return fft_res

def freq_to_mel(freq):
    return 2595 * np.log10(1 + freq / 700)

def mel_to_freq(mel):
    return 700 * (10**(mel / 2595) - 1)

def get_filter_points(fmin, fmax, filter_num, sample_rate, fft_size):
    fmin_mel = freq_to_mel(fmin)
    fmax_mel = freq_to_mel(fmax)

    mels = np.linspace(fmin_mel, fmax_mel, filter_num + 2)
    freqs = mel_to_freq(mels)

    return ((fft_size + 1) / sample_rate * freqs).astype(int),freqs

def get_filters(filter_points, fft_size):
    filters = np.zeros((len(filter_points) - 2, int(fft_size / 2) + 1))

    for i in range(len(filter_points) - 2):
        filters[i, filter_points[i]:filter_points[i+1]] = np.linspace(0, 1,filter_points[i+1] - filter_points[i])
        filters[i, filter_points[i+1]:filter_points[i+2]] = np.linspace(1, 0,filter_points[i+2] - filter_points[i+1])

    return filters
    
def dct(dct_filter_num, filter_len):
    basis = np.empty((dct_filter_num, filter_len))

    basis[0, :] = 1 / np.sqrt(filter_len)

    samples = np.arange(1,2*filter_len, 2) * np.pi / (filter_len * 2)

    for i in range(1,dct_filter_num):
        basis[i, :] = np.cos(i * samples) * np.sqrt(2 / filter_len)

    return basis

def mfcc(audio, sample_rate, fft_size, hop_size, dct_filter_num):
    audio = audio / np.max(np.abs(audio))
    audio_frames = framing(audio, sample_rate, hop_size, fft_size)

    window = get_window('hann', fft_size, fftbins=True)
    audio_window = audio_frames * window

    audio_fft = fast_fourier_transform(audio_window.T, fft_size)
    power_audio = np.square(np.abs(audio_fft))
    
    fmin = 0
    fmax = sample_rate / 2
    filter_num = 10

    filter_points, freqs = get_filter_points(fmin, fmax , filter_num, sample_rate, fft_size)
    filters = get_filters(filter_points, fft_size)
    enorm = 2 / (freqs[2:2+filter_num] - freqs[:filter_num])
    enorm = enorm[:, np.newaxis]
    filters *= enorm
    
    audio_filtered = np.dot(filters, power_audio)
    audio_filtered = np.where(audio_filtered == 0, np.finfo(float).eps, audio_filtered)  
    audio_log = 10 * np.log10(audio_filtered)
    dct_filters = dct(dct_filter_num, filter_num)
    cc = np.dot(dct_filters, audio_log)
    return cc


cepstral_coefficients = []
labels = []
specs = []

def f_high(y,sr):
    b,a = butter(10, 2000/(sr/2), btype='highpass')
    yf = lfilter(b,a,y)
    return yf
PATH = "./dataset/"

classes = os.listdir(PATH)


for idx, label in enumerate(classes):
    print("label",label)
    for i, file in enumerate(os.listdir(os.path.join(PATH, label))):
        signal, sample_rate = librosa.load(os.path.join(PATH, label, file), sr=44100, mono=True)
        
        audio = nr.reduce_noise(y=signal, sr=sample_rate, stationary=True, prop_decrease=0.9)
        audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=22050)
        
        
        spectrogram = np.abs(librosa.stft(audio, n_fft=2048, hop_length=512))
        cc = mfcc(audio, sample_rate, 2048, 25, 40)
        
        cepstral_coefficients.append(cc.flatten())
        labels.append(idx)
        

length_cc = [len(cc) for cc in cepstral_coefficients]
# print([c.shape for c in cepstral_coefficients])

df = pd.DataFrame([resample(x, num=int(max(length_cc))) for x in cepstral_coefficients])

df['label'] = labels
X = df.drop(columns=['label'], axis=0)
Y = df['label']

scaler = MinMaxScaler()
X = scaler.fit_transform(X)

pca = PCA(n_components=100)
X = pca.fit_transform(X)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = RandomForestClassifier()

param_grid = {
    'n_estimators':[None, 200],
    'criterion': ['gini', 'entropy', 'log_loss'],
    'max_features': ['sqrt', 'log2'], 
    'max_depth': [None,10,20],
    'min_samples_split': [2,3,5],
}

gsv = GridSearchCV(model, param_grid)
gsv.fit(x_train, y_train)
y_pred = gsv.predict(x_test)
print(classification_report(y_test, y_pred))
print(gsv.best_estimator_)
print(gsv.best_params_)

